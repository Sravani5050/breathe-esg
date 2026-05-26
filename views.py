from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Company, DataUpload, EmissionRecord, AuditLog
from .serializers import CompanySerializer, EmissionRecordSerializer
import pandas as pd
import io
from datetime import datetime

@api_view(['GET'])
def dashboard_stats(request):
    total = EmissionRecord.objects.count()
    pending = EmissionRecord.objects.filter(status='pending').count()
    approved = EmissionRecord.objects.filter(status='approved').count()
    flagged = EmissionRecord.objects.filter(status='flagged').count()
    suspicious = EmissionRecord.objects.filter(is_suspicious=True).count()
    return Response({
        'total': total,
        'pending': pending,
        'approved': approved,
        'flagged': flagged,
        'suspicious': suspicious,
    })

@api_view(['GET'])
def get_records(request):
    status_filter = request.GET.get('status', None)
    source_filter = request.GET.get('source', None)
    records = EmissionRecord.objects.all().order_by('-created_at')
    if status_filter:
        records = records.filter(status=status_filter)
    if source_filter:
        records = records.filter(source_type=source_filter)
    serializer = EmissionRecordSerializer(records, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def approve_record(request, record_id):
    try:
        record = EmissionRecord.objects.get(id=record_id)
        record.status = 'approved'
        record.save()
        AuditLog.objects.create(
            record=record,
            action='approved',
            changed_by='analyst',
            note=request.data.get('note', '')
        )
        return Response({'message': 'Record approved'})
    except EmissionRecord.DoesNotExist:
        return Response({'error': 'Not found'}, status=404)

@api_view(['POST'])
def flag_record(request, record_id):
    try:
        record = EmissionRecord.objects.get(id=record_id)
        record.status = 'flagged'
        record.save()
        AuditLog.objects.create(
            record=record,
            action='flagged',
            changed_by='analyst',
            note=request.data.get('note', '')
        )
        return Response({'message': 'Record flagged'})
    except EmissionRecord.DoesNotExist:
        return Response({'error': 'Not found'}, status=404)

@api_view(['POST'])
def upload_file(request):
    file = request.FILES.get('file')
    source_type = request.data.get('source_type')
    company_name = request.data.get('company', 'Demo Company')

    if not file or not source_type:
        return Response({'error': 'File and source_type required'}, status=400)

    company, _ = Company.objects.get_or_create(
        name=company_name,
        defaults={'industry': 'General'}
    )

    upload = DataUpload.objects.create(
        company=company,
        source_type=source_type,
        file_name=file.name,
    )

    try:
        df = pd.read_csv(io.StringIO(file.read().decode('utf-8')))
        records_created = 0

        for _, row in df.iterrows():
            EmissionRecord.objects.create(
                company=company,
                upload=upload,
                scope=int(row.get('scope', 1)),
                category=str(row.get('category', '')),
                description=str(row.get('description', '')),
                quantity=float(row.get('quantity', 0)),
                unit=str(row.get('unit', '')),
                co2_kg=float(row.get('co2_kg', 0)),
                source_type=source_type,
                record_date=row.get('date', datetime.today().date()),
                status='pending',
                is_suspicious=float(row.get('co2_kg', 0)) > 10000,
                suspicious_reason='CO2 value unusually high' if float(row.get('co2_kg', 0)) > 10000 else ''
            )
            records_created += 1

        upload.row_count = records_created
        upload.save()

        return Response({
            'message': f'{records_created} records uploaded successfully',
            'upload_id': upload.id
        })

    except Exception as e:
        return Response({'error': str(e)}, status=400)

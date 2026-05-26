from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=200)
    industry = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class DataUpload(models.Model):
    SOURCE_TYPES = [
        ('SAP', 'SAP Fuel/Procurement'),
        ('UTILITY', 'Utility/Electricity'),
        ('TRAVEL', 'Corporate Travel'),
    ]
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    source_type = models.CharField(max_length=20, choices=SOURCE_TYPES)
    file_name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    row_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.company} - {self.source_type}"

class EmissionRecord(models.Model):
    SCOPE_CHOICES = [(1,'Scope 1'),(2,'Scope 2'),(3,'Scope 3')]
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('flagged', 'Flagged'),
        ('rejected', 'Rejected'),
    ]
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    upload = models.ForeignKey(DataUpload, on_delete=models.CASCADE)
    scope = models.IntegerField(choices=SCOPE_CHOICES)
    category = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    quantity = models.FloatField()
    unit = models.CharField(max_length=50)
    co2_kg = models.FloatField()
    source_type = models.CharField(max_length=20)
    record_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_suspicious = models.BooleanField(default=False)
    suspicious_reason = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class AuditLog(models.Model):
    record = models.ForeignKey(EmissionRecord, on_delete=models.CASCADE)
    action = models.CharField(max_length=50)
    changed_by = models.CharField(max_length=100)
    note = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)


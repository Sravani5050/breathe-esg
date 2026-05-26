from django.contrib import admin
from .models import Company, DataUpload, EmissionRecord, AuditLog

admin.site.register(Company)
admin.site.register(DataUpload)
admin.site.register(EmissionRecord)
admin.site.register(AuditLog)
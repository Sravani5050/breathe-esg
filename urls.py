from django.contrib import admin
from django.urls import path
from ingestion import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/stats/', views.dashboard_stats),
    path('api/records/', views.get_records),
    path('api/records/<int:record_id>/approve/', views.approve_record),
    path('api/records/<int:record_id>/flag/', views.flag_record),
    path('api/upload/', views.upload_file),
]
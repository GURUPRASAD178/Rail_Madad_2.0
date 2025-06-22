from django.contrib import admin
from .models import Complaint

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('subject', 'email', 'pnr_number', 'category', 'created_at', 'is_resolved')
    list_filter = ('category', 'is_resolved')
    search_fields = ('subject', 'email', 'pnr_number')
    ordering = ('-created_at',)
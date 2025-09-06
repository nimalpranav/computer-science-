from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'assigned_to', 'deadline')
    search_fields = ('title', 'description')
    list_filter = ('deadline',)

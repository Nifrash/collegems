from django.contrib import admin
from .models import Lecturer


@admin.register(Lecturer)
class LecturerAdmin(admin.ModelAdmin):
    list_display = ('lecturer_id', 'user', 'department', 'specialization')
    readonly_fields = ('lecturer_id',)
    search_fields = ('lecturer_id', 'user__username', 'department', 'specialization')
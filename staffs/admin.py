from django.contrib import admin
from .models import Staff


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('staff_id', 'user', 'department', 'phone')
    readonly_fields = ('staff_id',)
    search_fields = ('staff_id', 'student_nic', 'user__username', 'department')
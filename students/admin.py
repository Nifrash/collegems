from django.contrib import admin
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'user', 'gender', 'admission_date')
    readonly_fields = ('student_id', 'admission_date')
    search_fields = ('student_id', 'user__username', 'user__first_name', 'user__last_name')
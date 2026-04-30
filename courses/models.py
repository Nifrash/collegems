from django.db import models
from college_management import settings
from lecturers.models import Lecturer

class Course(models.Model):
    course_code = models.CharField(max_length=20, unique=True, blank=True)
    course_name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    credits = models.IntegerField()
    course_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    lecturer = models.ForeignKey(
        Lecturer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def save(self, *args, **kwargs):
        if not self.course_code:
            super().save(*args, **kwargs)
            self.course_code = f"CRS.{self.pk:04d}"
            super().save(update_fields=['course_code'])
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.course_code} - {self.course_name}"

class Enrollment(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'STUDENT'}
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE
    )
    enrolled_date = models.DateField(auto_now_add=True)
    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student} - {self.course}"


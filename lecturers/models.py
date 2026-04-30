from django.db import models
from django.conf import settings
from accounts.utils import generate_custom_id


class Lecturer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    lecturer_id = models.CharField(max_length=20, unique=True, blank=True)
    department = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)

    def save(self, *args, **kwargs):
        if not self.lecturer_id:
            self.lecturer_id = generate_custom_id(Lecturer, 'lecturer_id', 'EUR.LEC')
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.lecturer_id} - {self.user.username}"
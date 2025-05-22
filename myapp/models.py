from django.db import models
from django.contrib.auth.models import User

class UserImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    original_image = models.ImageField(upload_to='uploads/')
    converted_image = models.ImageField(upload_to='converted/')
    direction = models.CharField(max_length=3, choices=[('A2B', 'A to B'), ('B2A', 'B to A')])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.direction} - {self.created_at}"
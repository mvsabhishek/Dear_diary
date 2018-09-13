from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Diary(models.Model):
    created_at = models.DateField(auto_now_add=True)
    title = models.CharField(max_length=200)
    body = models.TextField(max_length=10000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


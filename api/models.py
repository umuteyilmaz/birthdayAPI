from django.db import models

class User(models.Model):
    username = models.CharField(max_length=30, unique=True)
    birthday = models.DateField(null=True)
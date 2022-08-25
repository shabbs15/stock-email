from django.db import models

class User(models.Model):
    email = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=200)

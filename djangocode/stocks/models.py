from django.db import models

class User(models.Model):
    email = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=200)
    confirmed = models.BooleanField(default=False)

class EmailConfirmation(models.Model):
    email = models.ForeignKey(User, to_field="email", on_delete=models.CASCADE)
    emailHash = models.CharField(max_length=200)

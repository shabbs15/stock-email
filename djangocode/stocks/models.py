from django.db import models

class User(models.Model):
    email = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=200)
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.email + "\n " + self.password + "\n " + str(self.confirmed)

class EmailConfirmation(models.Model):
    email = models.ForeignKey(User, on_delete=models.CASCADE)
    emailHash = models.CharField(max_length=200)
    
    def __str__(self):
        return self.emailHash 

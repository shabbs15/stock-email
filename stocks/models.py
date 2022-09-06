from django.db import models

class Users(models.Model):
    email = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=200)
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.email + "\n " + self.password + "\n " + str(self.confirmed)

class EmailConfirmations(models.Model):
    email = models.ForeignKey(Users, on_delete=models.CASCADE)
    emailHash = models.CharField(max_length=200)
    
    def __str__(self):
        return self.emailHash 

class Stocks(models.Model):
    ticker = models.CharField(max_length=8, unique=True)
    percentage = models.FloatField(default=None, blank=True, null=True)
    users = models.ManyToManyField(Users)

    def __str__(self):
        return self.ticker + "\n" + str(self.percentage)

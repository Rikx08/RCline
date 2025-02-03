from django.db import models

class Tovars(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField()
    description = models.TextField()

class Users(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.TextField()
    password = models.TextField()
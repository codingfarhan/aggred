from django.db import models

# Create your models here.


class profile(models.Model):

    email = models.EmailField(unique=True)
    password = models.CharField(max_length=250)
    title = models.TextField(max_length=100)
    full_name = models.TextField(max_length=30)
    stars = models.IntegerField(default=0)
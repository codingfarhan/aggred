from django.db import models

# Create your models here.



class post(models.Model):

    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    user = models.CharField(max_length=30)
    user_image = models.TextField(default='default_url')
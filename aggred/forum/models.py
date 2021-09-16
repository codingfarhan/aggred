from django.db import models

# Create your models here.



class post(models.Model):

    post_id = models.TextField()

    user = models.CharField(max_length=30)
    user_image = models.TextField(default='default_url')

    
    title = models.TextField()
    content = models.TextField()

    # for gauging popularity of post
    likes = models.IntegerField(default=0)

    timestamp = models.DateTimeField(auto_now_add=True)
    answers = models.IntegerField(default=0)



class answer(models.Model):

    post_id = models.TextField()

    answer_id = models.TextField()

    user = models.CharField(max_length=30)

    content = models.TextField()

    timestamp = models.DateTimeField(auto_now_add=True)

    # answers will be arranged according to number of 'useful's 
    useful = models.IntegerField(default=0)



class reply(models.Model):

    post_id = models.TextField()

    answer_id = models.TextField()

    user = models.CharField(max_length=30)

    replying_to = models.CharField(max_length=30)

    content = models.TextField()

    timestamp = models.DateTimeField(auto_now_add=True)



from django.db import models

# Create your models here.



class post(models.Model):

    post_id = models.TextField(unique=True)

    email = models.CharField(max_length=30)
    user_image_url = models.TextField(default='default_url')
    full_name = models.CharField(max_length=30)
    user_title = models.TextField(default='')

    
    post_title = models.TextField()
    post_content = models.TextField()

    # for gauging popularity of post
    likes = models.IntegerField(default=0)

    post_date = models.DateTimeField(auto_now_add=True)
    
    answers = models.IntegerField(default=0)



class answer(models.Model):

    post_id = models.TextField(default='')

    answer_id = models.TextField(unique=True)

    full_name = models.CharField(max_length=30)

    user_title = models.TextField(default='')

    answer_content = models.TextField(default='')

    timestamp = models.DateTimeField(auto_now_add=True)

    # answers will be arranged according to number of 'useful's 
    votes = models.IntegerField(default=0)



class reply(models.Model):

    post_id = models.TextField()

    answer_id = models.TextField()

    reply_id = models.TextField(unique=True)

    
    email = models.CharField(max_length=30)
    user_image_url = models.TextField(default='default_url')
    full_name = models.CharField(max_length=30)


    reply_content = models.TextField()

    reply_date = models.DateTimeField(auto_now_add=True)



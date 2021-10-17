from django.db import models

# Create your models here.



class post(models.Model):

    post_id = models.TextField(unique=True)

    email = models.CharField(max_length=30, unique=False)
    user_image_url = models.TextField(default='https://t4.ftcdn.net/jpg/00/64/67/63/360_F_64676383_LdbmhiNM6Ypzb3FM4PPuFP9rHe7ri8Ju.jpg')
    full_name = models.CharField(max_length=30)
    user_title = models.TextField(default='')

    
    post_title = models.TextField()
    post_content = models.TextField()

    # for gauging popularity of post
    likes = models.IntegerField(default=0)

    post_date = models.DateTimeField(auto_now_add=True)
    
    answers = models.IntegerField(default=0)


    grade = models.CharField(default="None", max_length=10)
    degree = models.CharField(default="None", max_length=25)
    subject = models.CharField(default="None", max_length=20)





class answer(models.Model):

    post_id = models.TextField(default='')

    answer_id = models.TextField(unique=True)

    email = models.CharField(max_length=30, unique=True, default='')

    full_name = models.CharField(max_length=30)

    user_title = models.TextField(default='')

    user_image_url = models.TextField(default='https://t4.ftcdn.net/jpg/00/64/67/63/360_F_64676383_LdbmhiNM6Ypzb3FM4PPuFP9rHe7ri8Ju.jpg')

    answer_title = models.TextField(default='')

    answer_content = models.TextField(default='')

    timestamp = models.DateTimeField(auto_now_add=True)

    # answers will be arranged according to number of 'useful's 
    votes = models.IntegerField(default=0)





class reply(models.Model):

    post_id = models.TextField()

    answer_id = models.TextField()

    reply_id = models.TextField(unique=True)

    replying_to = models.CharField(max_length=30)

    
    email = models.CharField(max_length=30, default='')
    user_image_url = models.TextField(default='https://t4.ftcdn.net/jpg/00/64/67/63/360_F_64676383_LdbmhiNM6Ypzb3FM4PPuFP9rHe7ri8Ju.jpg')
    full_name = models.CharField(max_length=30)


    reply_content = models.TextField()

    reply_date = models.DateTimeField(auto_now_add=True)

    likes = models.IntegerField(default=0)

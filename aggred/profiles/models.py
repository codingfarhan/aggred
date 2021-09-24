from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager





class CustomAccountManager(BaseUserManager):


    def create_user(self, email, first_name, last_name, password, **other_fields):

        other_fields.setdefault('is_staff', False)
        other_fields.setdefault('is_superuser', False)

        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, **other_fields)

        user.set_password(password)

        user.save(using=self._db)

        return user


    def create_superuser(self, email, first_name, last_name, password, **other_fields):
            
            other_fields.setdefault('is_staff', True)
            other_fields.setdefault('is_superuser', True)
            other_fields.setdefault('is_active', True)


            if other_fields.get('is_staff') is not True:
                raise ValueError('Superuser has to be assigned is_staff = True')
            
            if other_fields.get('is_superuser') is  not True:
                raise ValueError('Superuser has to be assigned is_superuser = True')


            return self.create_user(email, first_name, last_name, password, social_user=False, **other_fields)





class profile(AbstractUser):

    username = None

    user_image_url = models.TextField(default='https://t4.ftcdn.net/jpg/00/64/67/63/360_F_64676383_LdbmhiNM6Ypzb3FM4PPuFP9rHe7ri8Ju.jpg')

    email = models.EmailField(unique=True)
    password = models.CharField(max_length=250)
    title = models.TextField(max_length=100)
    first_name = models.TextField(max_length=30)
    last_name = models.TextField(max_length=30)
    crowns = models.IntegerField(default=0)

    start_date = models.DateTimeField(auto_now_add=True)

    social_user = models.BooleanField(default=True)

    auth_token = models.TextField()

    is_verified = models.BooleanField(default=False)


    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomAccountManager()


    def __str__(self):
        return self.email





class save_post(models.Model):

    email = models.EmailField(max_length=30)
    post_id = models.TextField()
    saved_date = models.DateTimeField(auto_now_add=True)
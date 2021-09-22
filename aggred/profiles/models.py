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


            return self.create_user(email, first_name, last_name, password, **other_fields)





class profile(AbstractUser):

    email = models.EmailField(unique=True)
    password = models.CharField(max_length=250)
    title = models.TextField(max_length=100)
    full_name = models.TextField(max_length=30)
    crowns = models.IntegerField(default=0)

    start_date = models.DateTimeField(auto_now_add=True)


    USERNAME_FIELD = 'email'

    objects = CustomAccountManager()









class save_post(models.Models):

    email = models.EmailField(max_length=30)
    post_id = models.TextField()
    saved_date = models.DateTimeField(auto_now_add=True)
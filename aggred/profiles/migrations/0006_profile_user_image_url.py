# Generated by Django 3.2.7 on 2021-09-24 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0005_profile_social_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='user_image_url',
            field=models.TextField(default='https://t4.ftcdn.net/jpg/00/64/67/63/360_F_64676383_LdbmhiNM6Ypzb3FM4PPuFP9rHe7ri8Ju.jpg'),
        ),
    ]

# Generated by Django 3.2.7 on 2021-09-28 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0008_reply_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='degree',
            field=models.CharField(default='None', max_length=25),
        ),
        migrations.AddField(
            model_name='post',
            name='grade',
            field=models.CharField(default='None', max_length=10),
        ),
        migrations.AddField(
            model_name='post',
            name='subject',
            field=models.CharField(default='None', max_length=20),
        ),
    ]
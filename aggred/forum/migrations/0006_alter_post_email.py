# Generated by Django 3.2.7 on 2021-09-25 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0005_auto_20210925_1802'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='email',
            field=models.CharField(max_length=30),
        ),
    ]
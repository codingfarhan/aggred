# Generated by Django 3.2.7 on 2021-10-24 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0009_auto_20210928_1805'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='email',
            field=models.CharField(default='', max_length=30),
        ),
    ]

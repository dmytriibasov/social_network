# Generated by Django 4.2.7 on 2023-11-20 01:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='last_request_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]

# Generated by Django 3.0.5 on 2020-04-23 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('status', '0002_auto_20200423_0514'),
    ]

    operations = [
        migrations.AddField(
            model_name='status',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
    ]

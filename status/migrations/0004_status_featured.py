# Generated by Django 3.0.5 on 2020-04-23 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('status', '0003_status_is_staff'),
    ]

    operations = [
        migrations.AddField(
            model_name='status',
            name='featured',
            field=models.TextField(choices=[(1, 'Open'), (2, 'Close'), (3, 'Draft')], default=0),
        ),
    ]

# Generated by Django 4.2.2 on 2023-07-29 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('netmiko', '0002_device_device_name_device_platform_device_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='cpu_usage',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='device',
            name='interface_status',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='device',
            name='memory_usage',
            field=models.FloatField(blank=True, null=True),
        ),
    ]

# Generated by Django 4.2.2 on 2023-07-29 06:44

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('netmiko', '0003_device_cpu_usage_device_interface_status_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Alert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=100)),
                ('timestamp', models.DateTimeField(default=datetime.datetime.now)),
                ('details', models.TextField()),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='netmiko.device')),
            ],
        ),
    ]

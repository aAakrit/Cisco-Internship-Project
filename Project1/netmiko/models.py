from datetime import datetime
from django.db import models

class Device(models.Model):
    name = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField()
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    platform = models.CharField(max_length=50,default='Unknown')
    status = models.CharField(max_length=20,default='inactive')
    cpu_usage = models.FloatField(null=True, blank=True)
    memory_usage = models.FloatField(null=True, blank=True)
    interface_status = models.BooleanField(default=False)
    # Add additional fields for search and filtering
    device_name = models.CharField(max_length=100,default='Unknown')

    def __str__(self):
        return self.name

class Alert(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    type = models.CharField(max_length=100)
    timestamp = models.DateTimeField(default=datetime.now)
    details = models.TextField()

    def __str__(self):
        return f"{self.device.name} - {self.type} - {self.timestamp}"

class Configuration(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    config_details = models.TextField()

    def __str__(self):
        return f"Configuration for {self.device}"

class ParsedData(models.Model):
    configuration = models.ForeignKey(Configuration, on_delete=models.CASCADE)
    interface = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    description = models.CharField(max_length=100)

    def __str__(self):
        return f"Interface: {self.interface}, Status: {self.status}, Description: {self.description}"
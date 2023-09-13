from django import forms
from .models import Device, Configuration

class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ['name', 'ip_address', 'username', 'password']

class ConfigurationForm(forms.ModelForm):
    class Meta:
        model = Configuration
        fields = ['config_details']

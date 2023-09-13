import os
from django.shortcuts import render, get_object_or_404, redirect
from textfsm import TextFSM
from django.db.models import Q
from .models import Device, Configuration, ParsedData, Alert
#from netmiko import ConnectHandler
from .forms import DeviceForm, ConfigurationForm

'''def device_list(request):
    devices = Device.objects.all()
    return render(request, 'device_list.html', {'devices': devices})
'''
'''def device_detail(request, device_id):
    device = get_object_or_404(Device, pk=device_id)
    configurations = Configuration.objects.filter(device=device)
    return render(request, 'device_details.html', {'device': device, 'configurations': configurations})
'''

def device_health(request):
    devices = Device.objects.all()
    # In a real implementation, you would fetch the actual health information for each device.
    for device in devices:
        device.cpu_usage = 25.0
        device.memory_usage = 60.0
        device.interface_status = True  # Assume interfaces are up.
    return render(request, 'device_health.html', {'devices': devices})

def device_detail(request, device_id):
    device = get_object_or_404(Device, pk=device_id)
    configurations = Configuration.objects.filter(device=device)
    parsed_data = parse_configurations([config.config_details for config in configurations])
    return render(request, 'device_details.html', {'device': device, 'configurations': configurations, 'parsed_data': parsed_data})

def device_list(request):
    query = request.GET.get('q')
    devices = Device.objects.all()

    if query:
        devices = devices.filter(
            Q(name__icontains=query) |
            Q(ip_address__icontains=query) |
            Q(platform__icontains=query) |
            Q(status__icontains=query)
        )

    return render(request, 'device_list.html', {'devices': devices})

def device_create(request):
    if request.method == 'POST':
        form = DeviceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('device_list')
    else:
        form = DeviceForm()
    return render(request, 'device_create.html', {'form': form})

def device_update(request, device_id):
    device = get_object_or_404(Device, pk=device_id)
    if request.method == 'POST':
        form = DeviceForm(request.POST, instance=device)
        if form.is_valid():
            form.save()
            return redirect('device_detail', device_id=device_id)
    else:
        form = DeviceForm(instance=device)
    return render(request, 'device_update.html', {'form': form, 'device': device})

def device_delete(request, device_id):
    device = get_object_or_404(Device, pk=device_id)
    if request.method == 'POST':
        device.delete()
        return redirect('device_list')
    return render(request, 'device_delete.html', {'device': device})

def parse_configurations(configurations):
    template_path = os.path.join(os.path.dirname(__file__), 'textFSM_templates', 'interface.tpl')
    with open(template_path) as template_file:
        template = TextFSM(template_file)
        parsed_data = []
        for config in configurations:
            result = template.ParseText(config)
            parsed_data.extend(result)
        return parsed_data


def add_configuration(request, device_id):
    if request.method == 'POST':

        configuration = Configuration.objects.create(device_id=device_id, content=request.POST['content'])

        if configuration.violates_rules():
            Alert.objects.create(device=configuration.device, type='Configuration Issue', details='Configuration violates rules')

        return redirect('netmiko:device_detail', device_id=device_id)
    else:
        device = Device.objects.get(pk=device_id)
        return render(request, 'add_config.html', {'device': device})

# Problem with netmiko connecthandler

'''def add_configuration(request, device_id):
    device = get_object_or_404(Device, pk=device_id)
    
    if request.method == 'POST':
        form = ConfigurationForm(request.POST)
        if form.is_valid():
            configuration = form.save(commit=False)
            configuration.device = device
            
            # Connect to the device using Netmiko
            netmiko_device = {
                'device_type': 'cisco_ios',
                'ip': device.ip_address,
                'username': device.username,
                'password': device.password,
            }
            try:
                connection = ConnectHandler(**netmiko_device)
                output = connection.send_command(configuration.config_details)
                connection.disconnect()
                
                # Parse the output using TextFSM
                template_path = 'textFSM_templates/interface.tpl'
                with open(template_path) as template_file:
                    template = TextFSM(template_file)
                    parsed_data = template.ParseText(output)
                
                # Save the configuration and parsed data
                configuration.save()
                for data in parsed_data:
                    # Assuming the parsed data contains interface details
                    interface = data[0]
                    status = data[1]
                    description = data[2]
                    # Save the parsed data as well
                    # Modify this section based on your models and data structure
                    parsed_data_object = ParsedData.objects.create(configuration=configuration, interface=interface, status=status, description=description)
                
                return redirect('device_detail', device_id=device_id)
            except Exception as e:
                error_message = f"Error connecting to device: {str(e)}"
                return render(request, 'add_config.html', {'device': device, 'form': form, 'error_message': error_message})
    else:
        form = ConfigurationForm()
    
    return render(request, 'add_config.html', {'device': device, 'form': form})
'''

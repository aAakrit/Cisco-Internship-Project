from django.urls import path
from . import views

app_name='netmiko'

urlpatterns = [
    path('', views.device_list, name='device_list'),
    path('device/create/', views.device_create, name='device_create'),
    path('device/<int:device_id>/', views.device_detail, name='device_detail'),
    path('device/<int:device_id>/update/', views.device_update, name='device_update'),
    path('device/<int:device_id>/delete/', views.device_delete, name='device_delete'),
    path('device/health/',views.device_health, name='device_health'),
    path('device/<int:device_id>/add_configuration/', views.add_configuration, name='add_configuration'),
]

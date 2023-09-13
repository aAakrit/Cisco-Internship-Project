from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from . import views
from .views import  LoginView, ProtectedView, dashboard_view, registration_view

#app_name='Access'

urlpatterns = [
    #path('api/auth/', LoginRegistrationView.as_view(), name='api-auth'),
    path('api/protected/', ProtectedView.as_view(), name='api-protected'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('protected/', ProtectedView.as_view(), name='protected'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('', dashboard_view, name='dashboard'),
    path('register/', registration_view, name='register'),
    path('api/login/', LoginView.as_view(), name='api-login'),

    
]
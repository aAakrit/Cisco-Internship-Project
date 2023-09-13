from django.shortcuts import redirect, render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import authenticate, login
from Access.forms import RegisterUserForm

from Access.models import CustomUserProfile
from netmiko.models import Alert, Device


def registration_view(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, email=email, password=password)
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegisterUserForm()
    return render(request, 'register_user.html', {'form': form})

class LoginView(APIView):
    permission_classes = []

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            return Response({'refresh': str(refresh), 'access': str(refresh.access_token)})
        else:
            return Response({'error': 'Invalid credentials'}, status=400)

def dashboard_view(request):
    if request.user.is_authenticated:
        alerts = Alert.objects.all()[:5]  # Fetch the latest 5 alerts for the dashboard.
        num_alerts = Alert.objects.count()
        num_devices = Device.objects.count()
        paginator = Paginator(alerts, 10)
        page_number = request.GET.get('page')
        alerts_page = paginator.get_page(page_number)
        return render(request, 'home.html',{'alerts': alerts_page, 'num_devices': num_devices, 'num_alerts': num_alerts})
    else:
        return redirect('login')
    
class ProtectedView(APIView):
    def get(self, request):
        return Response({'message': 'You are authenticated!'})
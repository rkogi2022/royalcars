from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.urls import reverse_lazy

# Register view
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully. Please log in.')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

# Login view
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in successfully.')
            return redirect('car_list')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

# Logout view
def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('index')

# Forgot Password view
class ForgotPasswordView(PasswordResetView):
    template_name = 'forgot_password.html'
    email_template_name = 'password_reset_email.html'
    success_url = reverse_lazy('login')

# Reset Password view (built-in)
class ResetPasswordConfirmView(PasswordResetConfirmView):
    template_name = 'reset_password.html'
    success_url = reverse_lazy('login')

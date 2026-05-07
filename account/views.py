from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import CustomUserRegistrationForm

def register_view(request):
    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('frontend:home')
    else:
        form = CustomUserRegistrationForm()
    return render(request, 'account/register.html', {'form': form})

def login_view(request):
    return render(request, 'account/login.html')

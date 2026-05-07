from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

from .models import UserBankAccount


@login_required
def dashboard(request):

    return render(
        request,
        'customer/dashboard.html',
    )
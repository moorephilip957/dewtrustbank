from django.shortcuts import render

def home_view(request):
    return render(request, 'frontend/index.html')

def personal_view(request):
    return render(request, 'frontend/personal.html')

def corperate_view(request):
    return render(request, 'frontend/corperate.html')

def insurance_view(request):
    return render(request, 'frontend/insurance.html')

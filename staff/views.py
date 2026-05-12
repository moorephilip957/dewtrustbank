from django.shortcuts import render

def staff_dashboard(request):
    return render(request, 'staff/dashboard.html')
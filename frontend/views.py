from django.shortcuts import render,redirect
import time
def home_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('staff:staff_dashboard')
        else:
            return redirect('customer:dashboard')
    return render(request, 'frontend/index.html')

def personal_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('staff:staff_dashboard')
        else:
            return redirect('customer:dashboard')
    return render(request, 'frontend/personal.html')

def corperate_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('staff:staff_dashboard')
        else:
            return redirect('customer:dashboard')
    return render(request, 'frontend/corperate.html')

def insurance_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('staff:staff_dashboard')
        else:
            return redirect('customer:dashboard')
    return render(request, 'frontend/insurance.html')

def mortgages_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('staff:staff_dashboard')
        else:
            return redirect('customer:dashboard')
    return render(request, 'frontend/mortgages.html')

def savings_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('staff:staff_dashboard')
        else:
            return redirect('customer:dashboard')
    return render(request, 'frontend/seftons/savings.html')

def loans_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('staff:staff_dashboard')
        else:
            return redirect('customer:dashboard')
    return render(request, 'frontend/seftons/loans.html')

def cards_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('staff:staff_dashboard')
        else:
            return redirect('customer:dashboard')
    return render(request, 'frontend/seftons/cards.html')

def about_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('staff:staff_dashboard')
        else:
            return redirect('customer:dashboard')
    return render(request, 'frontend/seftons/about.html')

def contact_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('staff:staff_dashboard')
        else:
            return redirect('customer:dashboard')
    return render(request, 'frontend/seftons/contact.html')

def terms_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('staff:staff_dashboard')
        else:
            return redirect('customer:dashboard')
    return render(request, 'frontend/seftons/terms.html')
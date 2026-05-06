from django.shortcuts import render

def home_view(request):
    return render(request, 'frontend/index.html')

def personal_view(request):
    return render(request, 'frontend/personal.html')

def corperate_view(request):
    return render(request, 'frontend/corperate.html')

def insurance_view(request):
    return render(request, 'frontend/insurance.html')

def mortgages_view(request):
    return render(request, 'frontend/mortgages.html')

def savings_view(request):
    return render(request, 'frontend/seftons/savings.html')

def loans_view(request):
    return render(request, 'frontend/seftons/loans.html')

def cards_view(request):
    return render(request, 'frontend/seftons/cards.html')

def about_view(request):
    return render(request, 'frontend/seftons/about.html')

def contact_view(request):
    return render(request, 'frontend/seftons/contact.html')

def terms_view(request):
    return render(request, 'frontend/seftons/terms.html')
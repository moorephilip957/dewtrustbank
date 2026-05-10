from django.urls import path
from . import views

app_name = 'loan'  

urlpatterns = [
    path('apply-loan/', views.apply_loan, name='apply_loan'),
    path('loan-history/', views.loan_history, name='loan_history'),
]
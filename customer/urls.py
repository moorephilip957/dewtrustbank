from django.urls import path
from . import views

app_name = 'customer'  

urlpatterns = [
        path('dashboard/', views.dashboard, name='dashboard'), 
        path('transactions/', views.transaction_list, name='transactions'), 
        path('cards/', views.card, name='cards'), 
        path('local-transfer/', views.local_transfer, name='local_transfer'), 
        path('international-transfer/', views.international_transfer, name='international_transfer'), 
        path('deposit/', views.deposit, name='deposit'), 
        path('save-invest/', views.save_invest, name='save_invest'), 
        path('loan/', views.loan, name='loan'), 
        path('loan_history/', views.loan_history, name='loan_history'), 
        path('download_app/', views.download_app, name='download_app'), 
        path('settings/', views.settings, name='settings'), 
        path('support/', views.support, name='support'), 
        path('change_password/', views.change_password, name='change_password'), 
        path('apply_card/', views.apply_card, name='apply_card'), 
        path('payment/', views.payment, name='payment'),
        path("blocked/", views.account_blocked, name="blocked"),

        path("change-transaction-pin/", views.change_transaction_pin,name="change_transaction_pin"),
        path('change-password/', views.change_password, name='change_password'),
]
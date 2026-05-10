
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('frontend.urls', namespace="frontend")),
    path('auth/', include('account.urls', namespace="account")),
    path('account/', include('customer.urls', namespace="customer")),
    path('transaction/', include('transaction.urls', namespace="transaction")),
    path('loan/', include('loan.urls', namespace="loan")),
]

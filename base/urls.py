
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('frontend.urls', namespace="frontend")),
    path('auth/', include('account.urls', namespace="account")),
    path('account/', include('customer.urls', namespace="customer")),
    path('transaction/', include('transaction.urls', namespace="transaction")),
    path('loan/', include('loan.urls', namespace="loan")),
    path('support/', include('support.urls', namespace="support")),
    path('notification/', include('notification.urls', namespace="notification")),
    path('kyc/', include('kyc.urls', namespace="kyc")),
]
# urlpatterns += static(
#     settings.MEDIA_URL,
#     document_root=settings.MEDIA_ROOT
# )
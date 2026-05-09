from django.urls import path
from . import views

app_name = 'transaction'  

urlpatterns = [
    path('local-transfer/', views.local_transfer, name='local_transfer'),
    # path("transfer/success/<uuid:tx_id>/", views.success_view, name="transfer_success"),
    # path("transfer/pending/<uuid:tx_id>/", views.pending_view, name="transfer_pending"),
    # path("transfer/failed/<uuid:tx_id>/", views.failed_view, name="transfer_failed"),
]
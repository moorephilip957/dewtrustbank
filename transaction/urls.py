from django.urls import path
from . import views

app_name = 'transaction'  

urlpatterns = [
    path('local-transfer/', views.local_transfer, name='local_transfer'),
    path('wire-transfer/', views.wire_transfer, name='wire_transfer'),
    path("transfer/success/<int:tx_id>/", views.transfer_success, name="transfer_success"),
    path("transfer/pending/<int:tx_id>/", views.transfer_pending, name="transfer_pending"),
    path("transfer/failed/<int:tx_id>/", views.transfer_failed, name="transfer_failed"),
]
from django.urls import path
from . import views

app_name = 'transaction'  

urlpatterns = [
    path('local-transfer/', views.local_transfer, name='local_transfer'),
    path('wire-transfer/', views.wire_transfer, name='wire_transfer'),
    path("success/<int:tx_id>/", views.transfer_success, name="transfer_success"),
    path("pending/<int:tx_id>/", views.transfer_pending, name="transfer_pending"),
    path("failed/<int:tx_id>/", views.transfer_failed, name="transfer_failed"),

    # deposit
    path("deposit/", views.create_deposit, name="create_deposit"),
    path("deposit/<int:deposit_id>/", views.deposit_detail, name="deposit_detail"),
    path(
    "deposit/pending/<int:deposit_id>/",
        views.deposit_pending,
        name="deposit_pending"
    ),
]
from django.urls import path
from . import views

app_name = 'support'  

urlpatterns = [
    path("ticket/create/", views.create_ticket, name="create_ticket"),
    path("ticket/success/<str:reference_id>/", views.ticket_success, name="ticket_success"),
    path("tickets/", views.ticket_list, name="tickets"),
    path("tickets/<str:reference_id>/", views.ticket_detail, name="ticket_detail"),
]
from django.urls import path
from . import views

app_name = 'notification'
urlpatterns = [
    path('', views.notification_list, name='notification_list'),
    path('mark-all-read/', views.mark_all_notifications_read, name='mark_all_notifications_read'),
    path(
        "notifications/<int:pk>/read/",
        views.mark_notification_read,
        name="mark_read"
    )

]
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Notification


@login_required
def notification_list(request):
    notifications = request.user.notifications.all()
    unread_count = notifications.filter(read=False).count()
    return render(request, "notifications/notification_list.html", {
        "notifications": notifications,
        "unread_count": unread_count
    })


@login_required
def mark_all_notifications_read(request):
    request.user.notifications.filter(read=False).update(read=True)
    return redirect(request.META.get('HTTP_REFERER', 'notification:notification_list'))
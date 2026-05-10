# notifications/context_processors.py
from .models import Notification

def notifications_processor(request):
    if request.user.is_authenticated:
        notifications = request.user.notifications.order_by('-created_at')[:3]  # last 5 notifications
        unread_count = request.user.notifications.filter(read=False).count()
    else:
        notifications = []
        unread_count = 0
    return {
        'navbar_notifications': notifications,
        'navbar_unread_count': unread_count
    }
from django.shortcuts import render, redirect, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Notification
from kyc.decorator import kyc_required
from account.decorator import block_blocked_users

@login_required
@kyc_required
@block_blocked_users
def notification_list(request):
    notifications = request.user.notifications.all()
    unread_count = notifications.filter(read=False).count()
    return render(request, "notifications/notification_list.html", {
        "notifications": notifications,
        "unread_count": unread_count
    })


@login_required
@kyc_required
@block_blocked_users
def mark_all_notifications_read(request):

    if request.method == "POST":
        updated_count = request.user.notifications.filter(read=False).update(read=True)

        messages.success(
            request,
            f"{updated_count} notification(s) marked as read successfully."
        )

    return redirect(
        request.META.get('HTTP_REFERER', 'notification:notification_list')
    )


@login_required
@kyc_required
@block_blocked_users
def mark_notification_read(request, pk):
    notification = get_object_or_404(
        Notification,
        pk=pk,
        user=request.user
    )

    if not notification.read:
        notification.read = True
        notification.save(update_fields=["read"])

    return redirect("notification:notification_list")


@login_required
@kyc_required
@block_blocked_users
def delete_notification(request, pk):

    notification = get_object_or_404(
        Notification,
        pk=pk,
        user=request.user
    )

    if request.method == "POST":
        notification.delete()

        messages.success(
            request,
            "Notification deleted successfully."
        )

    return redirect("notification:notification_list")


@login_required
@kyc_required
@block_blocked_users
def delete_all_notifications(request):

    if request.method == "POST":

        deleted_count, _ = Notification.objects.filter(
            user=request.user
        ).delete()

        messages.success(
            request,
            f"{deleted_count} notification(s) deleted successfully."
        )

    return redirect("notification:notification_list")
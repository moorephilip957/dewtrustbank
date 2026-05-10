# notifications/utils.py
from django.contrib.contenttypes.models import ContentType
from .models import Notification

def create_notification(user, title, message, notif_type='info', related_object=None):
    """
    Create a notification for a user.
    """
    content_type = None
    object_id = None

    if related_object:
        content_type = ContentType.objects.get_for_model(related_object)  # <-- correct
        object_id = related_object.id

    return Notification.objects.create(
        user=user,
        title=title,
        message=message,
        notif_type=notif_type,
        content_type=content_type,
        object_id=object_id
    )


# how to use 
# from notifications.utils import create_notification

# # Example usage in a view
# create_notification(
#     user=request.user,
#     title+title
#     message="Your profile has been updated successfully",
#     notif_type="success"
# )


# from notifications.utils import create_notification
# from blog.models import Post

# post = Post.objects.get(pk=10)

# # Create a notification linked to this post
# create_notification(
#     user=request.user,
#     message="Your post was liked!",
#     notif_type="success",
#     related_object=post
# )
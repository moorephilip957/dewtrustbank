from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()


class Ticket(models.Model):
    PRIORITY_CHOICES = [
        ("low", "Low Priority - General inquiry"),
        ("medium", "Medium Priority - Standard issue"),
        ("high", "High Priority - Urgent matter"),
    ]

    STATUS_CHOICES = [
        ("open", "Open"),
        ("in_progress", "In Progress"),
        ("resolved", "Resolved"),
        ("closed", "Closed"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tickets")

    # ✅ Auto-generated reference ID
    reference_id = models.CharField(max_length=20, unique=True, blank=True, editable=False)

    name = models.CharField(max_length=150)
    email = models.EmailField()

    subject = models.CharField(max_length=255)
    message = models.TextField()

    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default="medium")
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default="open")

    category = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)

    attachment = models.FileField(upload_to="tickets/", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Generate reference ID only on first save
        if not self.reference_id:
            self.reference_id = self.generate_reference_id()
        super().save(*args, **kwargs)

    def generate_reference_id(self):
        from datetime import datetime
        date_part = datetime.now().strftime("%Y%m%d")
        unique_part = uuid.uuid4().hex[:6].upper()
        return f"TKT-{date_part}-{unique_part}"

    def __str__(self):
        return f"{self.subject} ({self.priority})"


class TicketMessage(models.Model):
    SENDER_CHOICES = [
        ("user", "User"),
        ("support", "Support"),
    ]

    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="messages")
    sender = models.CharField(max_length=10, choices=SENDER_CHOICES, default="user")
    content = models.TextField()
    attachment = models.FileField(upload_to="ticket_messages/", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.sender.capitalize()} message on {self.ticket.reference_id}"
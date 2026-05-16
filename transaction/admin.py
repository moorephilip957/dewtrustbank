# admin.py

from django.contrib import admin
from .models import TransactionHistory


@admin.register(TransactionHistory)
class TransactionHistoryAdmin(admin.ModelAdmin):
    list_display = (
        "amount",
        "created_at",
        "user",
        "reference",
    )

    search_fields = (
        "reference",
        "user__username",
        "user__email",
    )

    list_filter = (
        "transaction_type",
        "status",
        "direction",
        "created_at",
    )

    ordering = ("-created_at",)
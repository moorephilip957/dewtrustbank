from django.db import models

from account.models import CustomUser

class AccountFunding(models.Model):

    ADJUSTMENT_TYPES = [
        ('credit', 'Credit'),
        ('debit', 'Debit'),
    ]

    STATUS_CHOICES = [
        ('success', 'Success'),
        ('pending', 'Pending'),
        ('failed', 'Failed'),
    ]

    customer = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='account_fundings'
    )

    staff = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='staff_fundings'
    )

    transaction_type = models.CharField(
        max_length=20,
        choices=ADJUSTMENT_TYPES
    )

    amount = models.DecimalField(
        max_digits=20,
        decimal_places=2
    )

    description = models.TextField(
        blank=True
    )

    beneficiary_name = models.CharField(
        max_length=255,
        default='****self'
    )

    beneficiary_number = models.CharField(
        max_length=100,
        default='******self'
    )

    bank_name = models.CharField(
        max_length=255,
        default='Dew Trust Bank'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='success'
    )

    transaction_date = models.DateTimeField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return (
            f"{self.customer.username} - "
            f"{self.adjustment_type} - "
            f"{self.amount}"
        )
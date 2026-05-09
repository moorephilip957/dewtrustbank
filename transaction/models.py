# models.py
import random
import string
from django.db import models

from account.models import CustomUser


class TransactionHistory(models.Model):

    class TransactionType(models.TextChoices):
        DEPOSIT = "deposit", "Deposit"
        LOCAL_TRANSFER = "local_transfer", "Local Transfer"
        WIRE_TRANSFER = "wire_transfer", "Wire Transfer"
        WITHDRAWAL = "withdrawal", "Withdrawal"

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        SUCCESS = "success", "Success"
        FAILED = "failed", "Failed"

    class Direction(models.TextChoices):
        CREDIT = "credit", "Credit"
        DEBIT = "debit", "Debit"

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="transactions"
    )

    transaction_type = models.CharField(
        max_length=40,
        choices=TransactionType.choices
    )

    amount = models.DecimalField(
        max_digits=20,
        decimal_places=2
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )

    reference = models.CharField(
        max_length=120,
        unique=True,
        blank=True
    )

    direction = models.CharField(
        max_length=10,
        choices=Direction.choices
    )

    description = models.TextField(blank=True)

    balance_before = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0
    )

    balance_after = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0
    )

    beneficiary_name = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    beneficiary_number = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    bank_name = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def generate_reference(self):

        prefix = "TXN"

        random_part = ''.join(
            random.choices(
                string.ascii_uppercase + string.digits,
                k=10
            )
        )

        return f"{prefix}-{random_part}"

    def save(self, *args, **kwargs):

        # Auto-generate reference if not set
        if not self.reference:

            self.reference = self.generate_reference()

            # Ensure uniqueness
            while TransactionHistory.objects.filter(
                reference=self.reference
            ).exists():

                self.reference = self.generate_reference()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.reference


class Deposit(models.Model):

    class DepositMethod(models.TextChoices):
        BITCOIN = "BTC", "Bitcoin"
        USDT = "USDT", "USDT"
        WIRE = "WIRE", "Wire Transfer"

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        CONFIRMED = "confirmed", "Confirmed"

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE
    )

    method = models.CharField(
        max_length=20,
        choices=DepositMethod.choices
    )

    amount = models.DecimalField(
        max_digits=20,
        decimal_places=2
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )

    proof = models.ImageField(
        upload_to="deposit_proofs/",
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)


class CryptoWallet(models.Model):

    class Currency(models.TextChoices):
        BTC = "BTC", "Bitcoin"
        USDT = "USDT", "USDT"

    currency = models.CharField(
        max_length=10,
        choices=Currency.choices
    )

    wallet_address = models.CharField(max_length=255)

    qr_code = models.ImageField(
        upload_to="wallet_qr/"
    )

    network = models.CharField(
        max_length=30,
        blank=True
    )

    active = models.BooleanField(default=True)

    def __str__(self):
        return self.currency
    

class LocalTransfer(models.Model):

    class TransferType(models.TextChoices):
        IMMEDIATE = "immediate", "Immediate"
        SCHEDULED = "scheduled", "Scheduled"

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE
    )

    beneficiary_name = models.CharField(max_length=255)

    beneficiary_number = models.CharField(max_length=20)

    bank_name = models.CharField(max_length=255)

    transfer_type = models.CharField(
        max_length=30,
        choices=TransferType.choices
    )

    amount = models.DecimalField(
        max_digits=20,
        decimal_places=2
    )

    description = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        default="pending"
    )

    transaction = models.OneToOneField(
        TransactionHistory,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)


class InternationalTransfer(models.Model):

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE
    )

    beneficiary_name = models.CharField(max_length=255)

    beneficiary_number = models.CharField(max_length=50)

    bank_name = models.CharField(max_length=255)

    bank_address = models.TextField()

    country = models.CharField(max_length=120)

    swift_code = models.CharField(max_length=20)

    iban_number = models.CharField(max_length=50)

    amount = models.DecimalField(
        max_digits=20,
        decimal_places=2
    )

    description = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        default="pending"
    )

    transaction = models.OneToOneField(
        TransactionHistory,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
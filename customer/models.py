from django.db import models
from django.contrib.auth.hashers import (
    make_password,
    check_password, 
    identify_hasher
)
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from decimal import Decimal
import random
import string
from django.utils import timezone
from datetime import timedelta

from account.models import CustomUser


class BankAccountType(models.Model):
    name = models.CharField(max_length=200, unique=True)

    daily_transfer_limit = models.DecimalField(max_digits=15, decimal_places=2)
    single_transfer_limit = models.DecimalField(max_digits=15, decimal_places=2)
    minimum_balance = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )
    allows_overdraft = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class UserBankAccount(models.Model):
    """Bank account model linked to CustomUser with secure transaction PIN."""

    ACCOUNT_STATUS = [
        ('success', 'Success'),
        ('pending', 'Pending'),
        ('failed', 'Failed'),
    ]

    CURRENCIES = [
        ('USD', 'US Dollar ($)'),
        ('EUR', 'Euro (€)'),
        ('GBP', 'British Pound (£)'),
        ('CAD', 'Canadian Dollar (C$)'),
        ('AUD', 'Australian Dollar (A$)'),

        # Dubai / UAE
        ('AED', 'UAE Dirham (د.إ)'),

        # Kuwait
        ('KWD', 'Kuwaiti Dinar (د.ك)'),

        # Japan
        ('JPY', 'Japanese Yen (¥)'),

        # South Korea
        ('KRW', 'South Korean Won (₩)'),
    ]

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='bank_account',
        verbose_name=_('user')
    )

    account_number = models.CharField(
        _('account number'),
        max_length=20,
        unique=True,
        editable=False,
        blank=True,
        help_text=_('Auto-generated unique account number')
    )

    account_type = models.ForeignKey(
        BankAccountType,
        on_delete=models.PROTECT,
        related_name='accounts'
    )

    currency = models.CharField(
        _('currency'),
        max_length=3,
        choices=CURRENCIES,
        default='USD'
    )

    balance = models.DecimalField(
        _('balance'),
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text=_('Current account balance')
    )

    transaction_pin = models.CharField(
        _('transaction PIN'),
        max_length=128,
        blank=True,
        null=True,
        help_text=_(
            '4-6 digit PIN for authorizing transactions (hashed)'
        )
    )

    transaction_status = models.CharField(
        max_length=10,
        choices=ACCOUNT_STATUS,
        default='success'
    )

    payment_reference = models.CharField(
        max_length=12,
        # unique=True,
        blank=True,
        editable=False
    )

    sort_code = models.CharField(
        max_length=8,
        # unique=True,
        blank=True,
        editable=False
    )

    is_active = models.BooleanField(_('active'), default=True)

    account_age = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(
        _('created at'),
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        _('updated at'),
        auto_now=True
    )

    class Meta:
        verbose_name = _('Bank Account')
        verbose_name_plural = _('Bank Accounts')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['account_number']),
            models.Index(fields=['user', 'is_active']),
        ]

    def __str__(self):
        return (
            f"{self.account_type.name} - "
            f"{self.account_number} ({self.currency})"
        )

    def save(self, *args, **kwargs):
        """Auto-generate account number on first save."""

        if not self.account_number:
            self.account_number = self.generate_account_number()

        if not self.payment_reference:
            self.payment_reference = self.generate_payment_reference()

        if not self.sort_code:
            self.sort_code = self.generate_sort_code()

        # Hash PIN only if not already hashed
        if self.transaction_pin:

            try:
                identify_hasher(self.transaction_pin)

            except Exception:
                self.transaction_pin = make_password(
                    str(self.transaction_pin)
                )

        super().save(*args, **kwargs)

    def generate_account_number(self):
        """Generate a unique account number."""

        prefix = "DTB"

        while True:
            random_digits = ''.join(
                random.choices(string.digits, k=10)
            )

            account_number = f"{random_digits}"
            # account_number = f"{prefix}{random_digits}"

            exists = UserBankAccount.objects.filter(
                account_number=account_number
            ).exists()

            if not exists:
                return account_number
            
    def generate_payment_reference(self):
        """Generate unique payment reference (e.g. PR-8H3K9D2F1L)."""

        prefix = "PR"

        while True:
            random_part = ''.join(
                random.choices(string.ascii_uppercase + string.digits, k=10)
            )

            ref = f"{prefix}-{random_part}"

            if not UserBankAccount.objects.filter(payment_reference=ref).exists():
                return ref
            

    def generate_sort_code(self):
        """Generate bank-style sort code (e.g. 12-34-56)."""

        while True:
            sort_code = f"{random.randint(10,99)}-{random.randint(10,99)}-{random.randint(10,99)}"

            if not UserBankAccount.objects.filter(sort_code=sort_code).exists():
                return sort_code

    # =========================
    # PIN METHODS
    # =========================

    def set_transaction_pin(self, raw_pin):
        """Securely set a new transaction PIN."""

        if not self._validate_pin_format(raw_pin):
            raise ValidationError(
                _('PIN must be 4-6 numeric digits')
            )

        self.transaction_pin = make_password(str(raw_pin))
        self.save()

    def check_transaction_pin(self, raw_pin):
        """Verify a PIN against the stored hash."""

        if not self.transaction_pin:
            return False

        return check_password(
            str(raw_pin),
            self.transaction_pin
        )

    def _validate_pin_format(self, pin):
        """Validate PIN is 4-6 numeric digits."""

        return (
            pin is not None
            and str(pin).isdigit()
            and 4 <= len(str(pin)) <= 6
        )

    # =========================
    # DISPLAY HELPERS
    # =========================

    def get_currency_symbol(self):
        """Return currency symbol."""

        symbols = {
            'USD': '$',
            'EUR': '€',
            'GBP': '£',
            'CAD': 'C$',
            'AUD': 'A$',

            # UAE / Dubai
            'AED': 'د.إ',

            # Kuwait
            'KWD': 'د.ك',

            # Japan
            'JPY': '¥',

            # South Korea
            'KRW': '₩',
        }

        return symbols.get(self.currency, self.currency)

    def formatted_balance(self):
        """Return formatted balance."""

        return (
            f"{self.get_currency_symbol()}"
            f"{self.balance:,.2f}"
        )


class DebitCard(models.Model):

    CARD_TYPES = [
        ('visa', 'Visa Debit Card'),
        ('master', 'Master Debit Card'),
    ]

    CARD_STATUS = [
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('blocked', 'Blocked'),
        ('expired', 'Expired'),
    ]

    CURRENCIES = [
        ('USD', 'USD - US Dollar'),
        ('EUR', 'EUR - Euro'),
        ('GBP', 'GBP - British Pound'),
        ('AED', 'AED - UAE Dirham'),
        ('KWD', 'KWD - Kuwaiti Dinar'),
    ]

    account = models.ForeignKey(
        'UserBankAccount',
        on_delete=models.CASCADE,
        related_name='cards'
    )

    card_type = models.CharField(
        max_length=20,
        choices=CARD_TYPES,
        default='visa'
    )

    currency = models.CharField(
        max_length=10,
        choices=CURRENCIES,
        default='USD'
    )

    card_number = models.CharField(
        max_length=19,
        unique=True,
        editable=False
    )

    card_holder_name = models.CharField(
        max_length=150
    )

    expiry_date = models.DateField()

    cvv = models.CharField(
        max_length=4
    )

    spending_limit = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00
    )

    balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00
    )

    issuance_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00
    )

    status = models.CharField(
        max_length=20,
        choices=CARD_STATUS,
        default='pending'
    )

    is_virtual = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def generate_card_number(self):
        return f"5355 {random.randint(1000,9999)} {random.randint(1000,9999)} {random.randint(1000,9999)}"

    def generate_cvv(self):
        return str(random.randint(100, 999))

    def save(self, *args, **kwargs):

        if not self.card_number:
            self.card_number = self.generate_card_number()

        if not self.cvv:
            self.cvv = self.generate_cvv()

        if not self.expiry_date:
            self.expiry_date = timezone.now().date() + timedelta(days=1460)

        if not self.card_holder_name:
            self.card_holder_name = self.account.user.get_full_name()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.card_holder_name} - {self.card_number}"


class DebitCardApplication(models.Model):
    CARD_TYPES = [
        ('visa', 'Visa Debit Card'),
        ('master', 'Master Debit Card'),
    ]

    DELIVERY_METHODS = [
        ('pickup', 'Branch Pickup'),
        ('home_delivery', 'Home Delivery'),
    ]

    CURRENCIES = [
        ('USD', 'USD - US Dollar'),
        ('EUR', 'EUR - Euro'),
        ('GBP', 'GBP - British Pound'),
        ('AED', 'AED - UAE Dirham'),
        ('KWD', 'KWD - Kuwaiti Dinar'),
    ]

    ISSUANCE_FEES = [
        ('5', 'Standard - $5.00'),
        ('15', 'Gold - $15.00'),
        ('25', 'Platinum - $25.00'),
        ('50', 'Black - $50.00'),
    ]

    APPLICATION_STATUS = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('declined', 'Declined'),
    ]

    # User ForeignKey
    account = models.ForeignKey(
        UserBankAccount,
        on_delete=models.CASCADE,
        related_name='debit_card_applications'
    )

    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()

    card_type = models.CharField(
        max_length=20,
        choices=CARD_TYPES
    )

    currency = models.CharField(
        max_length=10,
        choices=CURRENCIES,
        default='USD'
    )

    spending_limit = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="Daily or monthly spending limit"
    )

    issuance_fee = models.CharField(
        max_length=10,
        choices=ISSUANCE_FEES,
        default='5'
    )

    delivery_method = models.CharField(
        max_length=20,
        choices=DELIVERY_METHODS
    )

    status = models.CharField(
        max_length=20,
        choices=APPLICATION_STATUS,
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.card_type}"
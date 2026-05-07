from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from decimal import Decimal
import random
import string

from account.models import CustomUser


class BankAccountType(models.Model):
    name = models.CharField(max_length=20, unique=True)

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

    # ACCOUNT_TYPES = [
    #     ('savings', _('Savings Account')),
    #     ('checking', _('Checking Account')),
    #     ('business', _('Business Account')),
    #     ('virtual', _('Virtual Account')),
    # ]

    CURRENCIES = [
        ('USD', 'US Dollar ($)'),
        ('EUR', 'Euro (€)'),
        ('GBP', 'British Pound (£)'),
        ('NGN', 'Nigerian Naira (₦)'),
        ('GHS', 'Ghanaian Cedi (₵)'),
        ('ZAR', 'South African Rand (R)'),
        ('CAD', 'Canadian Dollar (C$)'),
        ('AUD', 'Australian Dollar (A$)'),
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

    is_active = models.BooleanField(_('active'), default=True)

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

        # Hash PIN if plain text
        if (
            self.transaction_pin
            and len(self.transaction_pin) <= 6
            and not self.transaction_pin.startswith('pbkdf2_')
        ):
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

            account_number = f"{prefix}{random_digits}"

            exists = UserBankAccount.objects.filter(
                account_number=account_number
            ).exists()

            if not exists:
                return account_number

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
            'NGN': '₦',
            'GHS': '₵',
            'ZAR': 'R',
            'CAD': 'C$',
            'AUD': 'A$',
        }

        return symbols.get(self.currency, self.currency)

    def formatted_balance(self):
        """Return formatted balance."""

        return (
            f"{self.get_currency_symbol()}"
            f"{self.balance:,.2f}"
        )
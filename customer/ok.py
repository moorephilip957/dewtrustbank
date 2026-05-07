from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from decimal import Decimal
import random
import string
from .models import CustomUser  # Your custom user model

class UserBankAccount(models.Model):
    """Bank account model linked to CustomUser with secure transaction PIN."""
    
    # Account Types
    ACCOUNT_TYPES = [
        ('savings', _('Savings Account')),
        ('checking', _('Checking Account')),
        ('business', _('Business Account')),
        ('virtual', _('Virtual Account')),
    ]
    
    # Supported Currencies (ISO 4217)
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

    # 🔗 One-to-One Link to CustomUser
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='bank_account',
        verbose_name=_('user')
    )
    
    # Account Details
    account_number = models.CharField(
        _('account number'),
        max_length=20,
        unique=True,
        editable=False,
        help_text=_('Auto-generated unique account number')
    )
    
    account_type = models.CharField(
        _('account type'),
        max_length=20,
        choices=ACCOUNT_TYPES,
        default='savings'
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
    
    # 🔐 Secure Transaction PIN (hashed, never stored in plain text)
    transaction_pin = models.CharField(
        _('transaction PIN'),
        max_length=128,  # Hashed length
        blank=True,
        null=True,
        help_text=_('4-6 digit PIN for authorizing transactions (hashed)')
    )
    
    # Metadata
    is_active = models.BooleanField(_('active'), default=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        verbose_name = _('Bank Account')
        verbose_name_plural = _('Bank Accounts')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['account_number']),
            models.Index(fields=['user', 'is_active']),
        ]

    def __str__(self):
        return f"{self.get_account_type_display()} - {self.account_number} ({self.currency})"

    def save(self, *args, **kwargs):
        """Auto-generate account number on first save."""
        if not self.account_number:
            self.account_number = self._generate_account_number()
        
        # Hash transaction PIN if it's being set/changed and is plain text
        if self.transaction_pin and len(self.transaction_pin) <= 6 and not self.transaction_pin.startswith('pbkdf2_'):
            self.transaction_pin = make_password(self.transaction_pin)
            
        super().save(*args, **kwargs)

    def _generate_account_number(self, length=10):
        """Generate a unique numeric account number."""
        while True:
            # Format: 3-digit bank code + random digits
            prefix = "PMX"  # Your company prefix (PMX Precious Metals)
            random_digits = ''.join(random.choices(string.digits, k=length))
            account_num = f"{prefix}{random_digits}"
            
            if not UserBankAccount.objects.filter(account_number=account_num).exists():
                return account_num

    # 🔐 PIN Methods
    def set_transaction_pin(self, raw_pin):
        """Securely set a new transaction PIN."""
        if not self._validate_pin_format(raw_pin):
            raise ValidationError(_('PIN must be 4-6 numeric digits'))
        self.transaction_pin = make_password(str(raw_pin))
        self.save(update_fields=['transaction_pin'])

    def check_transaction_pin(self, raw_pin):
        """Verify a PIN against the stored hash."""
        if not self.transaction_pin:
            return False
        return check_password(str(raw_pin), self.transaction_pin)

    def _validate_pin_format(self, pin):
        """Validate PIN is 4-6 numeric digits."""
        return pin is not None and str(pin).isdigit() and 4 <= len(str(pin)) <= 6

    # 💰 Transaction Methods
    def deposit(self, amount, description="", reference=None):
        """Add funds to the account. Returns Transaction object."""
        if amount <= 0:
            raise ValidationError(_('Deposit amount must be positive'))
        
        self.balance += Decimal(str(amount))
        self.save(update_fields=['balance'])
        
        return Transaction.objects.create(
            account=self,
            transaction_type='credit',
            amount=amount,
            balance_after=self.balance,
            description=description or _('Deposit'),
            reference=reference,
            status='completed'
        )

    def withdraw(self, amount, pin, description="", reference=None):
        """Withdraw funds with PIN verification. Returns Transaction object."""
        if amount <= 0:
            raise ValidationError(_('Withdrawal amount must be positive'))
        if amount > self.balance:
            raise ValidationError(_('Insufficient funds'))
        if not self.check_transaction_pin(pin):
            raise ValidationError(_('Invalid transaction PIN'))
        
        self.balance -= Decimal(str(amount))
        self.save(update_fields=['balance'])
        
        return Transaction.objects.create(
            account=self,
            transaction_type='debit',
            amount=amount,
            balance_after=self.balance,
            description=description or _('Withdrawal'),
            reference=reference,
            status='completed',
            pin_verified=True
        )

    def get_currency_symbol(self):
        """Return currency symbol for display."""
        symbols = {
            'USD': '$', 'EUR': '€', 'GBP': '£', 'NGN': '₦',
            'GHS': '₵', 'ZAR': 'R', 'CAD': 'C$', 'AUD': 'A$'
        }
        return symbols.get(self.currency, self.currency)

    def formatted_balance(self):
        """Return balance with currency symbol."""
        return f"{self.get_currency_symbol()}{self.balance:,.2f}"
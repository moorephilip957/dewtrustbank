from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField

class CustomUserManager(BaseUserManager):
    """Custom manager for creating users and superusers with email as the primary identifier."""
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, username, password, **extra_fields)

class CustomUser(AbstractUser):
    SMS_ALERT_CHOICES = (
        ('activate', 'Activate'),
        ('deactivate', 'Deactivate'),
    )

    STATUS_CHOICES = (
        ('active', 'Active'),
        ('blocked', 'Blocked'),
    )
    # Override email to enforce uniqueness (AbstractUser leaves it blank by default)
    email = models.EmailField(_('email address'), unique=True)
    middle_name = models.CharField(_('middle name'), max_length=150, blank=True, null=True)
    phone_number = models.CharField(_('phone number'), max_length=20, blank=True)
    country = CountryField(blank=True)
    sms_alert = models.CharField(
        max_length=20,
        choices=SMS_ALERT_CHOICES,
        default='deactivate'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active'
    )

    objects = CustomUserManager()

    # 🔑 Email is now the authentication field
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    @property
    def full_name(self):
        """Combines first, middle, and last names, ignoring blanks/None."""
        parts = [self.first_name, self.last_name]
        # parts = [self.first_name, self.middle_name, self.last_name]
        return ' '.join(part for part in parts if part)

    def __str__(self):
        return self.email
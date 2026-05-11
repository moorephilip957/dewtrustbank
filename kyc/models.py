from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth import get_user_model

User = get_user_model()

class KYCVerification(models.Model):

    TITLE_CHOICES = [
        ('mr', 'Mr'),
        ('mrs', 'Mrs'),
        ('miss', 'Miss'),
        ('dr', 'Dr'),
        ('prof', 'Prof'),
    ]

    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    ACCOUNT_TYPE_CHOICES = [
        ('savings', 'Savings'),
        ('current', 'Current'),
        ('business', 'Business'),
    ]

    EMPLOYMENT_TYPE_CHOICES = [
        ('employed', 'Employed'),
        ('self_employed', 'Self Employed'),
        ('student', 'Student'),
        ('unemployed', 'Unemployed'),
    ]

    SALARY_RANGE_CHOICES = [
        ('0-10000', '$0 - $10,000'),
        ('10000-50000', '$10,000 - $50,000'),
        ('50000-100000', '$50,000 - $100,000'),
        ('100000+', '$100,000+'),
    ]

    DOCUMENT_TYPE_CHOICES = [
        ('passport', 'International Passport'),
        ('national_id', 'National ID'),
        ('drivers_license', 'Drivers License'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    # =========================
    # Personal Details
    # =========================
    user = models.OneToOneField(User, related_name="kycverification", on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)

    title = models.CharField(
        max_length=20,
        choices=TITLE_CHOICES
    )

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES
    )

    zipcode = models.CharField(max_length=20)

    date_of_birth = models.DateField()

    # =========================
    # Employment Information
    # =========================

    ssn = models.CharField(
        max_length=100,
        verbose_name="State Security Number"
    )

    account_type = models.CharField(
        max_length=30,
        choices=ACCOUNT_TYPE_CHOICES
    )

    employment_type = models.CharField(
        max_length=30,
        choices=EMPLOYMENT_TYPE_CHOICES
    )

    annual_income_range = models.CharField(
        max_length=30,
        choices=SALARY_RANGE_CHOICES
    )

    # =========================
    # Address Information
    # =========================

    address_line = models.TextField()

    city = models.CharField(max_length=100)

    state = models.CharField(max_length=100)

    nationality = models.CharField(max_length=100)

    # =========================
    # Next of Kin
    # =========================

    beneficiary_legal_name = models.CharField(max_length=255)

    next_of_kin_address = models.TextField()

    relationship = models.CharField(max_length=100)

    age = models.PositiveIntegerField()

    # =========================
    # Document Upload
    # =========================

    document_type = models.CharField(
        max_length=30,
        choices=DOCUMENT_TYPE_CHOICES
    )

    upload_front_side = models.ImageField(
        upload_to='kyc/front/',
        # validators=[
        #     FileExtensionValidator(
        #         allowed_extensions=['jpg', 'jpeg', 'png', 'gif']
        #     )
        # ]
    )

    upload_back_side = models.ImageField(
        upload_to='kyc/back/',
        # validators=[
        #     FileExtensionValidator(
        #         allowed_extensions=['jpg', 'jpeg', 'png', 'gif']
        #     )
        # ]
    )

    passport_photograph = models.ImageField(
        upload_to='kyc/passport/',
        # validators=[
        #     FileExtensionValidator(
        #         allowed_extensions=['jpg', 'jpeg', 'png', 'gif']
        #     )
        # ]
    )

    verified = models.BooleanField(default=False)
    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='pending'
    )


    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name
    
    @property
    def is_kyc_verified(self):
        """
        Returns True if KYC is approved and verified
        """
        return self.verified and self.status == 'approved'
    
    @property
    def is_kyc_locked(self):
        """
        Returns True if KYC should NOT be editable (pending or approved)
        """
        return self.status in ["pending", "approved"]
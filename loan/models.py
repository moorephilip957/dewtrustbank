# models.py

from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


class LoanApplication(models.Model):

    LOAN_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('processing', 'Processing'),
        ('rejected', 'Rejected'),
        ('disbursed', 'Disbursed'),
        ('repaid', 'Repaid'),
    ]

    CREDIT_FACILITY_CHOICES = [
        ('personal', 'Personal Loan'),
        ('business', 'Business Loan'),
        ('mortgage', 'Mortgage Loan'),
        ('education', 'Education Loan'),
        ('car', 'Car Loan'),
    ]

    INCOME_RANGE_CHOICES = [
        ('below_2000', 'Below $2,000'),
        ('2000_5000', '$2,000 - $5,000'),
        ('5000_10000', '$5,000 - $10,000'),
        ('above_10000', 'Above $10,000'),
    ]

    applicant = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='loan_applications'
    )

    loan_type = models.CharField(
        max_length=50,
        choices=CREDIT_FACILITY_CHOICES
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="Loan Amount in USD"
    )

    duration_months = models.PositiveIntegerField(
        help_text="Loan duration in months"
    )

    purpose = models.TextField(
        help_text="Describe the purpose of the loan"
    )

    monthly_net_income = models.CharField(
        max_length=50,
        choices=INCOME_RANGE_CHOICES
    )

    annual_interest_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )

    interest_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    total_repayment = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    monthly_payment = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    amount_paid = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    remaining_balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    due_date = models.DateField(
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=LOAN_STATUS_CHOICES,
        default='pending'
    )

    date_applied = models.DateTimeField(
        auto_now_add=True
    )

    def get_interest_rate(self):

        if self.duration_months <= 6:
            return Decimal('8.0')

        elif self.duration_months <= 12:
            return Decimal('12.0')

        elif self.duration_months <= 24:
            return Decimal('15.0')

        return Decimal('18.0')

    def calculate_loan(self):

        principal = Decimal(self.amount)

        self.annual_interest_rate = self.get_interest_rate()

        rate = Decimal(self.annual_interest_rate)

        time_in_years = Decimal(self.duration_months) / Decimal(12)

        # SIMPLE INTEREST
        interest = (
            principal *
            rate *
            time_in_years
        ) / Decimal(100)

        total = principal + interest

        monthly = total / Decimal(self.duration_months)

        self.interest_amount = round(interest, 2)

        self.total_repayment = round(total, 2)

        self.monthly_payment = round(monthly, 2)

        self.remaining_balance = round(total - self.amount_paid, 2)

        self.due_date = (
            timezone.now().date() +
            timedelta(days=self.duration_months * 30)
        )

    def save(self, *args, **kwargs):

        self.calculate_loan()

        super().save(*args, **kwargs)

    def __str__(self):

        return f"{self.applicant.username} - ${self.amount}"


class Repayment(models.Model):

    loan = models.ForeignKey(
        LoanApplication,
        on_delete=models.CASCADE,
        related_name='repayments'
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    payment_date = models.DateTimeField(
        auto_now_add=True
    )

    reference = models.CharField(
        max_length=200,
        unique=True
    )

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)

        loan = self.loan

        total_paid = sum(
            payment.amount
            for payment in loan.repayments.all()
        )

        loan.amount_paid = total_paid

        loan.remaining_balance = (
            loan.total_repayment - Decimal(total_paid)
        )

        if loan.remaining_balance <= 0:
            loan.status = 'repaid'

        loan.save()

    def __str__(self):

        return f"{self.loan.applicant.username} - ${self.amount}"
from django.contrib import admin
from .models import BankAccountType, UserBankAccount


# =========================
# BANK ACCOUNT TYPE ADMIN
# =========================
@admin.register(BankAccountType)
class BankAccountTypeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'daily_transfer_limit',
        'single_transfer_limit',
        'minimum_balance',
        'activation_fee',
        'allows_overdraft',
    )

    search_fields = ('name',)

    list_filter = ('allows_overdraft',)

    ordering = ('name',)

    fieldsets = (
        ('Account Type Info', {
            'fields': ('name',)
        }),
        ('Limits', {
            'fields': (
                'daily_transfer_limit',
                'single_transfer_limit',
                'minimum_balance',
                'allows_overdraft',
                'activation_fee',
            )
        }),
    )


# =========================
# USER BANK ACCOUNT ADMIN
# =========================
@admin.register(UserBankAccount)
class UserBankAccountAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'account_number',
        'account_type',
        'currency',
        'balance',
        'transaction_status',
        'is_active',
        'created_at',
    )

    list_filter = (
        'account_type',
        'currency',
        'is_active',
        'created_at',
    )

    search_fields = (
        'account_number',
        'user__email',
        'user__username',
    )

    readonly_fields = (
        'account_number',
        'balance',
        'created_at',
        'updated_at',
    )

    fieldsets = (
        ('User Info', {
            'fields': ('user', 'account_number')
        }),
        ('Account Details', {
            'fields': ('account_type', 'currency', 'balance', 'is_active')
        }),
        ('Security', {
            'fields': ('transaction_pin',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
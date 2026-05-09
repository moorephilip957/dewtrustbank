from django.db import transaction
from django.core.exceptions import ValidationError
from .results import TransactionResult


class TransactionProcessor:

    @staticmethod
    def process(account, amount, user_status, transaction_obj):

        # ❌ FAILED USER
        if user_status == "failed":

            transaction_obj.status = "failed"
            transaction_obj.save()

            return TransactionResult(
                status="failed",
                message="User not eligible for transactions",
                transaction=transaction_obj
            )

        # 🟡 PENDING USER (HOLD FUNDS)
        if user_status == "pending":

            if account.available_balance < amount:

                return TransactionResult(
                    status="failed",
                    message="Insufficient balance",
                    transaction=transaction_obj
                )

            with transaction.atomic():

                account.balance -= amount
                account.save()

                transaction_obj.status = "pending"
                transaction_obj.save()

            return TransactionResult(
                status="pending",
                message="Transaction pending approval",
                transaction=transaction_obj
            )

        # 🟢 SUCCESS USER
        if user_status == "success":

            if account.balance < amount:

                return TransactionResult(
                    status="failed",
                    message="Insufficient balance",
                    transaction=transaction_obj
                )

            with transaction.atomic():

                account.balance -= amount
                # account.ledger_balance -= amount
                account.save()

                transaction_obj.status = "success"
                transaction_obj.save()

            return TransactionResult(
                status="success",
                message="Transaction completed successfully",
                transaction=transaction_obj
            )
from .utils import generate_reference
from .processors import TransactionProcessor
from .models import TransactionHistory


def create_transaction(
    user,
    account,
    amount,
    transaction_type,
    direction,
    bank_name,
    beneficiary_name="",
    beneficiary_number="",
    description=""
):

    transaction_obj = TransactionHistory.objects.create(
        user=user,
        amount=amount,
        transaction_type=transaction_type,
        direction=direction,
        description=description,
        reference=generate_reference(),
        status="pending",

        # Beneficiary Details
        beneficiary_name=beneficiary_name,
        beneficiary_number=beneficiary_number,
        bank_name=bank_name,
    )

    result = TransactionProcessor.process(
        account=account,
        amount=amount,
        user_status=account.transaction_status,
        transaction_obj=transaction_obj
    )

    return result
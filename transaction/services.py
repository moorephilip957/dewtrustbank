from .utils import generate_reference
from .processors import TransactionProcessor
from .models import TransactionHistory


def create_transaction(user, account, amount, transaction_type, direction, description=""):

    transaction_obj = TransactionHistory.objects.create(
        user=user,
        amount=amount,
        transaction_type=transaction_type,
        direction=direction,
        description=description,
        reference=generate_reference(),
        status="pending"
    )

    result = TransactionProcessor.process(
        account=account,
        amount=amount,
        user_status=user.status,
        transaction_obj=transaction_obj
    )

    return result
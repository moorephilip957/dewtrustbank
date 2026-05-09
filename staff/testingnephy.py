def admin_deposit_user(request, user_id):

    user = User.objects.get(id=user_id)
    account = Account.objects.get(user=user)

    amount = Decimal(request.POST["amount"])

    return create_transaction(
        user=user,
        account=account,
        amount=amount,
        transaction_type="deposit",
        direction="credit",
        description="Admin credit",
        initiated_by="system"
    )



def admin_withdraw_user(request, user_id):

    user = User.objects.get(id=user_id)
    account = Account.objects.get(user=user)

    amount = Decimal(request.POST["amount"])

    return create_transaction(
        user=user,
        account=account,
        amount=amount,
        transaction_type="withdrawal",
        direction="debit",
        description="Admin debit",
        initiated_by="system"
    )
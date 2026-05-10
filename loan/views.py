from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import LoanApplicationForm
from .models import LoanApplication


@login_required
def apply_loan(request):
    active_loans = LoanApplication.active_loans_count(request.user)
    
    print(active_loans)

    if request.method == 'POST':
        form = LoanApplicationForm(request.POST)

        if form.is_valid():
            loan = form.save(commit=False)

            # attach logged-in user
            loan.applicant = request.user

            loan.save()

            messages.success(request, "Loan application submitted successfully!")

            return redirect('loan:apply_loan')

        else:
            messages.error(request, "Please correct the errors below.")

    else:
        form = LoanApplicationForm()

    return render(request, 'loan/apply_loan.html', {
        'form': form,
        "active_loans": active_loans
    })


@login_required
def loan_history(request):

    status = request.GET.get('status')

    loans = LoanApplication.objects.filter(
        applicant=request.user
    )

    if status:
        loans = loans.filter(status=status)

    loans = loans.order_by('-date_applied')

    return render(request, 'loan/loan_history.html', {
        'loans': loans,
        'status': status
    })
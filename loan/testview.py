# views.py

from django.shortcuts import render, redirect
from .forms import LoanApplicationForm


def apply_loan(request):
    if request.method == 'POST':
        form = LoanApplicationForm(request.POST)

        if form.is_valid():
            loan = form.save(commit=False)
            loan.applicant = request.user
            loan.save()

            return redirect('success_page')

    else:
        form = LoanApplicationForm()

    return render(request, 'loan_form.html', {'form': form})



# views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import LoanApplicationForm


@login_required
def apply_loan(request):

    if request.method == 'POST':

        form = LoanApplicationForm(request.POST)

        if form.is_valid():

            loan = form.save(commit=False)

            loan.applicant = request.user

            loan.save()

            return redirect('success_page')

    else:

        form = LoanApplicationForm()

    return render(
        request,
        'loan_form.html',
        {'form': form}
    )
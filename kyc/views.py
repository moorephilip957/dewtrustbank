from django.shortcuts import render, redirect
from .forms import KYCVerificationForm


def kyc_verification(request):

    if request.method == 'POST':
        form = KYCVerificationForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():
            form.save()
            return redirect('success_page')

    else:
        form = KYCVerificationForm()

    return render(
        request,
        'kyc/verification.html',
        {'form': form}
    )
from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import KYCVerificationForm
from .models import KYCVerification
from .decorator import kyc_block_if_approved


@kyc_block_if_approved
def kyc_terms(request):

    return render(
        request,
        'kyc/terms.html',
    )


@kyc_block_if_approved
def kyc_verification(request):

    # try to get existing KYC (edit mode)
    try:
        kyc_instance = request.user.kycverification
        is_edit = True
    except KYCVerification.DoesNotExist:
        kyc_instance = None
        is_edit = False

    # 🔒 BLOCK EDITING IF APPROVED
    if kyc_instance and kyc_instance.status == "approved":
        messages.info(request, "Your KYC is already approved and cannot be edited.")
        return redirect("customer:dashboard")

    if request.method == 'POST':

        form = KYCVerificationForm(
            request.POST,
            request.FILES,
            instance=kyc_instance
        )

        if form.is_valid():
            kyc = form.save(commit=False)
            kyc.user = request.user  
            kyc.save()

            if is_edit:
                messages.success(request, "Your KYC request has been edited successfully. You will be notified once the review process is complete.")
            else:
                messages.success(request, "Your KYC request has been submitted successfully. You will be notified once the review process is complete.")

            return redirect('kyc:kyc_verification')

    else:
        form = KYCVerificationForm(instance=kyc_instance)

    return render(request, 'kyc/verification.html', {
        'form': form,
        'is_edit': is_edit
    })
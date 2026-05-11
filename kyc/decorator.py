from functools import wraps
from django.shortcuts import redirect

def kyc_required(view_func):

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        # 1. must be logged in
        if not request.user.is_authenticated:
            return redirect('account:login')

        # 2. check KYC existence
        try:
            kyc = request.user.kycverification
        except:
            return redirect('kyc:kyc_terms')

        # 3. handle KYC states

        # not submitted yet
        if kyc.status is None:
            return redirect('kyc:kyc_terms')

        # pending review → block access, send to KYC page
        if kyc.status == "pending":
            return redirect('kyc:kyc_verification')

        # rejected → allow resubmission via KYC page
        if kyc.status == "rejected":
            return redirect('kyc:kyc_verification')

        # approved → full access
        if kyc.status == "approved" and kyc.is_kyc_verified:
            return view_func(request, *args, **kwargs)

        # fallback safety
        return redirect('kyc:kyc_verification')

    return wrapper


def kyc_block_if_approved(view_func):

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        # must be logged in
        if not request.user.is_authenticated:
            return redirect('account:login')

        # safely get kyc
        try:
            kyc = request.user.kycverification
        except:
            kyc = None

        # if KYC exists and approved → block access to KYC pages
        if kyc and kyc.status == "approved" and kyc.is_kyc_verified:
            return redirect('customer:dashboard')

        return view_func(request, *args, **kwargs)

    return wrapper
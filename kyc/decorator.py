from django.shortcuts import redirect


def kyc_required(view_func):

    def wrapper(request, *args, **kwargs):

        if not hasattr(request.user, 'kyc'):
            return redirect('kyc_verification')

        if not request.user.kyc.is_kyc_verified:
            return redirect('kyc_verification')

        return view_func(request, *args, **kwargs)

    return wrapper


# usage
# from .decorators import kyc_required


# @kyc_required
# def dashboard(request):
#     return render(request, 'dashboard.html')
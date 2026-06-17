import random

from otp.models import OTP


def generate_otp(user, otp_type='login'):

    # invalidate previous login OTPs

    OTP.objects.filter(
        user=user,
        otp_type=otp_type,
        is_used=False
    ).update(is_used=True)

    code = str(
        random.randint(100000, 999999)
    )

    otp = OTP.objects.create(
        user=user,
        code=code,
        otp_type=otp_type
    )

    return otp
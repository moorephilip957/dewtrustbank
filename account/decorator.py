from functools import wraps
from django.shortcuts import redirect


def block_blocked_users(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        # Ensure user is authenticated
        if request.user.is_authenticated:

            # Redirect blocked users
            if request.user.status == "blocked":
                return redirect("account:blocked")

        return view_func(request, *args, **kwargs)

    return wrapper


# from django.shortcuts import render
# from .decorators import block_blocked_users


# @block_blocked_users
# def dashboard(request):
#     return render(request, "dashboard.html")
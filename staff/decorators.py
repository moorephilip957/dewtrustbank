from django.http import HttpResponseForbidden
from functools import wraps


def staff_required(view_func):

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        if request.user.is_authenticated and request.user.is_staff:
            return view_func(request, *args, **kwargs)

        return HttpResponseForbidden(
            """
            <h1>403 Forbidden</h1>
            <p>You are not authorized to access this page.</p>
            """
        )

    return wrapper
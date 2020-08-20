from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test

def peserta_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, name='login'):

    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_peserta,
        login_url = login_url,
        redirect_field_name = redirect_field_name

    )
    if function:
        return actual_decorator(function)
    return actual_decorator

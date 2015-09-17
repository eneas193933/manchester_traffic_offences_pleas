from django.contrib.auth.decorators import user_passes_test


def court_staff_user_required(function):
    def _test_func(user):
        return user.has_perm("plea.court_staff_user") or user.is_superuser

    return user_passes_test(_test_func)(function)


def court_admin_user_required(function):
    def _test_func(user):
        return user.has_perm("plea.court_staff_admin") or user.is_superuser

    return user_passes_test(_test_func)(function)

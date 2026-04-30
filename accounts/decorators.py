from django.contrib.auth.decorators import user_passes_test


def role_required(role):
    def check(user):
        return user.is_authenticated and (user.is_superuser or user.role == role)
    return user_passes_test(check)
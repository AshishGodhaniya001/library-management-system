from django.core.exceptions import PermissionDenied

def is_librarian_or_admin(user):
    if not user.is_authenticated:
        return False
    # Agar user ke paas role field hai
    role = getattr(user, "role", None)
    if role in ["librarian", "admin"]:
        return True
    # Agar Django staff/superuser hai to bhi allow
    if user.is_staff or user.is_superuser:
        return True
    return False

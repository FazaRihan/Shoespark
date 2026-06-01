from django.contrib.auth.backends import ModelBackend
from .models import Account

from django.contrib.auth.backends import ModelBackend
from .models import Account

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # Support both 'email' kwarg and 'username' (untuk admin)
        email = kwargs.get('email') or username
        
        if email is None or password is None:
            return None
        
        try:
            user = Account.objects.get(email=email)
        except Account.DoesNotExist:
            return None
        
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
    
    def get_user(self, user_id):
        try:
            return Account.objects.get(pk=user_id)
        except Account.DoesNotExist:
            return None
    
    def user_can_authenticate(self, user):
        # Override: cek is_active
        return getattr(user, 'is_active', False)
__author__ = 'Bertrand'
from bbc_auth.views.serializers.lm_password_reset_serializer import LMPasswordResetSerializer
from rest_auth.views import PasswordResetView

class LMPasswordResetView(PasswordResetView):
    serializer_class = LMPasswordResetSerializer


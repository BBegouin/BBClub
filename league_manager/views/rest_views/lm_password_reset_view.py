__author__ = 'Bertrand'
from rest_framework.generics import GenericAPIView
from league_manager.views.serializers.lm_password_reset_serializer import LMPasswordResetSerializer
from rest_auth.views import PasswordResetView

class LMPasswordResetView(PasswordResetView):
    serializer_class = LMPasswordResetSerializer


__author__ = 'Bertrand'
from bbc_auth.views.serializers.bbc_password_reset_serializer import BBCPasswordResetSerializer
from rest_auth.views import PasswordResetView

class BBCPasswordResetView(PasswordResetView):
    serializer_class = BBCPasswordResetSerializer



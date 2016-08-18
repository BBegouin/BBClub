__author__ = 'Bertrand'
from bbc_auth.views.serializers.bbc_registration_serializer import BBCRegsitrationSerializer
from rest_auth.registration.views import RegisterView

class BBCRegistrationView(RegisterView):
    serializer_class = BBCRegsitrationSerializer



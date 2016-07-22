__author__ = 'Bertrand'
from rest_auth.serializers import PasswordResetSerializer

class LMPasswordResetSerializer(PasswordResetSerializer):

    def get_email_options(self):
         opts = { 'extra_email_context':{'test':'test_value'}}
         return opts

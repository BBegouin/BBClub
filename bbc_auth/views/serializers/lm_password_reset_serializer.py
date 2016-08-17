__author__ = 'Bertrand'
from rest_auth.serializers import PasswordResetSerializer
from django.conf import settings

class LMPasswordResetSerializer(PasswordResetSerializer):

    def get_email_options(self):
        front_domain=getattr(settings,"FRONT_DOMAIN")
        opts = {    'html_email_template_name':'registration/password_reset_email.html',
                    'extra_email_context':{'reset_url':'front/resetpwd',
                                           'front_domain':front_domain}}
        return opts

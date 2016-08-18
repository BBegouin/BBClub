__author__ = 'Bertrand'
from rest_auth.serializers import PasswordResetSerializer
from rest_framework import serializers
from django.conf import settings

class BBCPasswordResetSerializer(PasswordResetSerializer):

    resetUrl = serializers.URLField(max_length=200, min_length=None, allow_blank=False)

    def get_email_options(self):
        front_domain=getattr(settings,"FRONT_DOMAIN")

        request = self.context.get('request')

        opts = {'html_email_template_name':'registration/password_reset_email.html',
                'extra_email_context': {'reset_url': self.initial_data['resetUrl']}}
        return opts

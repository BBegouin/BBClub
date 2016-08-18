__author__ = 'Bertrand'

from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings

class BBCAccountAdapter(DefaultAccountAdapter):

    def get_email_confirmation_url(self, request, emailconfirmation):
        """Constructs the email confirmation (activation) url."""

        url = "http://{front_domain}/front/confirm_email/{key}".format(
            front_domain=getattr(settings,"FRONT_DOMAIN"),
            key=emailconfirmation.key)

        return url
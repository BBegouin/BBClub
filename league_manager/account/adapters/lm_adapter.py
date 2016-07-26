__author__ = 'Bertrand'
from allauth.utils import build_absolute_uri
from django.core.urlresolvers import reverse
from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings

class LM_Adapter(DefaultAccountAdapter):

    def get_email_confirmation_url(self, request, emailconfirmation):
        """Constructs the email confirmation (activation) url.

        Note that if you have architected your system such that email
        confirmations are sent outside of the request context `request`
        can be `None` here.
        """
        url = "http://{front_domain}/front/confirm_email/{key}".format(
            front_domain=getattr(settings,"FRONT_DOMAIN"),
            key=emailconfirmation.key)

        return url
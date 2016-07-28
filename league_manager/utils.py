__author__ = 'Bertrand'

from django.utils.six.moves.urllib.parse import urlsplit
from django.conf import settings

def build_front_uri(location, protocol=None):
    domain = getattr(settings, "FRONT_DOMAIN", None)
    bits = urlsplit(location)
    if not (bits.scheme and bits.netloc):
        uri = '{proto}://{domain}{url}'.format(
            proto=account_settings.DEFAULT_HTTP_PROTOCOL,
            domain=site.domain,
            url=location)
    else:
        uri = location


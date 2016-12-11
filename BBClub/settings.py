
from __future__ import absolute_import, unicode_literals
import os

EXEC_PROFILE = os.environ.get('EXEC_PROFILE','dev')
print('EXEC PROFILE : %s =====================================',EXEC_PROFILE)
#si on est en prod...
if EXEC_PROFILE == 'prod' :
    print('================= PROOOOOOOOOOOOOOOD ====================')
    from BBClub.prod_settings import *
elif EXEC_PROFILE == 'dev' :
    from BBClub.local_settings import *


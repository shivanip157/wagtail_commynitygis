from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '3-0#p%pjwc9k4ss)cmu3+32ch8ts6+4i9+ma^wj63(g$fuxsw_'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['10.129.133.223','127.0.0.1', 'localhost','*'] 

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


try:
    from .local import *
except ImportError:
    pass

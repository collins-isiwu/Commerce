from .settings import *

SECRET_KEY = '6ps8j!crjgrxt34cqbqn7x&b3y%(fny8k8nh21+qa)%ws3fh!q'

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

MIGRATION_MODULES = {
    'auctions': 'auctions.migrations_dev'
}

# Media files (Images stored in db and the system)
MEDIA_URL = '/media_dev/'
MEDIA_ROOT = BASE_DIR / 'media_dev'
from . import *
import dj_database_url


# Global config for production on Heroku

# Secret key is set as a env variable -> heroku config: set SECRET_KEY=YOUR_SECRET_KEY
# Do not forget to set as an env variable DJANGO_SETTINGS_MODULE -> heroku config: set DJANGO_SETTINGS_MODULE='fitperf.settings.heroku'

SECRET_KEY = os.environ['SECRET_KEY']
DEBUG = False
ALLOWED_HOSTS = ['fitperf.herokuapp.com']

# For static management during production

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    os.path.join(BASE_DIR, "program_builder/static"),
    os.path.join(PROJECT_ROOT, 'static'),
]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)
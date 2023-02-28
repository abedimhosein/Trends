from django.apps import AppConfig
from django.conf import settings


class HashtagsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'trends.hashtags'

    def ready(self):
        if settings.USE_APPS_SIGNAL:
            import trends.hashtags.signals

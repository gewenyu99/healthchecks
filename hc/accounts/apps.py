from django.apps import AppConfig
from django.conf import settings

import posthog


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.AutoField"
    name = "hc.accounts"

    def ready(self) -> None:
        posthog.api_key = settings.POSTHOG_PROJECT_TOKEN
        posthog.host = settings.POSTHOG_HOST
        posthog.enable_exception_autocapture = True

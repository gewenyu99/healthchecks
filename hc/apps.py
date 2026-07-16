import atexit

from django.apps import AppConfig
from django.conf import settings


class HcConfig(AppConfig):
    name = "hc"

    def ready(self) -> None:
        from posthog import Posthog

        self.posthog_client = Posthog(
            project_api_key=settings.POSTHOG_PROJECT_TOKEN,
            host=settings.POSTHOG_HOST,
            enable_exception_autocapture=True,
        )
        atexit.register(self.posthog_client.shutdown)

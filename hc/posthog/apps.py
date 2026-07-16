import atexit

from django.apps import AppConfig
from django.conf import settings

posthog_client = None


class PosthogConfig(AppConfig):
    name = "hc.posthog"

    def ready(self) -> None:
        import posthog

        global posthog_client
        posthog_client = posthog.Posthog(
            project_api_key=settings.POSTHOG_PROJECT_TOKEN,
            host=settings.POSTHOG_HOST,
            enable_exception_autocapture=True,
        )
        atexit.register(posthog_client.shutdown)

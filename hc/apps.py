import atexit

from django.apps import AppConfig
from django.conf import settings


class PostHogConfig(AppConfig):
    name = "hc"

    def ready(self) -> None:
        from posthog import Posthog

        if not settings.POSTHOG_PROJECT_TOKEN:
            raise RuntimeError("POSTHOG_PROJECT_TOKEN must be configured")

        self.posthog = Posthog(
            project_api_key=settings.POSTHOG_PROJECT_TOKEN,
            host=settings.POSTHOG_HOST,
            enable_exception_autocapture=True,
        )
        atexit.register(self.posthog.shutdown)

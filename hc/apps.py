"""Application configuration for shared PostHog instrumentation."""

import atexit

from django.apps import AppConfig
from django.conf import settings


class HealthchecksConfig(AppConfig):
    name = "hc"

    def ready(self) -> None:
        """Initialize the shared PostHog client when Django starts."""
        from posthog import Posthog

        from hc import posthog_client

        posthog_client.client = Posthog(
            project_api_key=settings.POSTHOG_PROJECT_TOKEN,
            host=settings.POSTHOG_HOST,
            enable_exception_autocapture=True,
        )
        atexit.register(posthog_client.client.shutdown)

from __future__ import annotations

import atexit

from django.apps import AppConfig
from django.conf import settings

posthog_client = None


class PosthogConfig(AppConfig):
    name = "hc.posthog"

    def ready(self) -> None:
        from posthog import Posthog

        global posthog_client
        posthog_client = Posthog(
            project_api_key=settings.POSTHOG_PROJECT_TOKEN,
            host=settings.POSTHOG_HOST,
            enable_exception_autocapture=True,
        )
        atexit.register(posthog_client.shutdown)

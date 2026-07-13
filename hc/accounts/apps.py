from __future__ import annotations

import atexit

from django.apps import AppConfig
from django.conf import settings


class AccountsConfig(AppConfig):
    name = "hc.accounts"

    def ready(self) -> None:
        if not settings.POSTHOG_PROJECT_TOKEN:
            return

        import posthog
        from posthog import Posthog

        posthog.project_api_key = settings.POSTHOG_PROJECT_TOKEN
        posthog.host = settings.POSTHOG_HOST
        posthog.default_client = Posthog(
            project_api_key=settings.POSTHOG_PROJECT_TOKEN,
            host=settings.POSTHOG_HOST,
            enable_exception_autocapture=True,
            debug=settings.DEBUG,
        )
        atexit.register(posthog.default_client.shutdown)

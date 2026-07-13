from __future__ import annotations

import atexit

from django.apps import AppConfig
from django.conf import settings
from posthog import Posthog


class FrontConfig(AppConfig):
    name = "hc.front"
    posthog_client: Posthog

    def ready(self) -> None:
        self.posthog_client = Posthog(
            project_api_key=settings.POSTHOG_PROJECT_TOKEN,
            host=settings.POSTHOG_HOST,
            enable_exception_autocapture=True,
        )
        settings.POSTHOG_MW_CLIENT = self.posthog_client
        atexit.register(self.posthog_client.shutdown)

    @classmethod
    def get_posthog_client(cls) -> Posthog:
        return cls.posthog_client

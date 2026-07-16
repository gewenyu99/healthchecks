from __future__ import annotations

import atexit

from django.apps import AppConfig
from django.conf import settings


class HealthchecksConfig(AppConfig):
    name = "hc"

    def ready(self) -> None:
        from posthog import Posthog

        self.posthog_client = Posthog(
            project_api_key=settings.POSTHOG_PROJECT_TOKEN,
            host=settings.POSTHOG_HOST,
            enable_exception_autocapture=True,
        )
        atexit.register(self.posthog_client.shutdown)

        from django.contrib.auth.signals import user_logged_in

        def identify_user(sender, request, user, **kwargs) -> None:
            self.posthog_client.set(
                distinct_id=str(user.id),
                properties={
                    "email": user.email,
                },
            )

        user_logged_in.connect(
            identify_user,
            dispatch_uid="hc.posthog.identify_user",
            weak=False,
        )

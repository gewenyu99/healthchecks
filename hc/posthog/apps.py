from __future__ import annotations

import atexit

from django.apps import AppConfig
from django.conf import settings
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from posthog import Posthog, identify_context, new_context

posthog_client: Posthog


class PosthogConfig(AppConfig):
    name = "hc.posthog"

    def ready(self) -> None:
        global posthog_client

        posthog_client = Posthog(
            project_api_key=settings.POSTHOG_PROJECT_TOKEN,
            host=settings.POSTHOG_HOST,
            enable_exception_autocapture=True,
        )
        atexit.register(posthog_client.shutdown)

        @receiver(user_logged_in, dispatch_uid="hc.posthog.identify_logged_in_user")
        def identify_logged_in_user(sender, request, user, **kwargs) -> None:
            with new_context():
                identify_context(str(user.pk))
                posthog_client.set(
                    distinct_id=str(user.pk),
                    properties={"email": user.email},
                )

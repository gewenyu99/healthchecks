from __future__ import annotations

import atexit

from django.conf import settings
from posthog import Posthog

client = Posthog(
    project_api_key=settings.POSTHOG_PROJECT_TOKEN,
    host=settings.POSTHOG_HOST,
    enable_exception_autocapture=True,
)
atexit.register(client.shutdown)


def capture(user_id: int | str, event: str, properties: dict[str, object] | None = None) -> None:
    client.capture(str(user_id), event, properties=properties or {})

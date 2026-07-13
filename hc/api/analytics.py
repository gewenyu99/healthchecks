from __future__ import annotations

from typing import Any

from posthog import Posthog

posthog_client: Posthog | None = None


def set_client(client: Posthog) -> None:
    global posthog_client
    posthog_client = client


def capture_event(distinct_id: str, event: str, properties: dict[str, Any]) -> None:
    if posthog_client is not None:
        posthog_client.capture(
            distinct_id=distinct_id,
            event=event,
            properties=properties,
        )


def set_person_properties(distinct_id: str, properties: dict[str, Any]) -> None:
    if posthog_client is not None:
        posthog_client.set(distinct_id=distinct_id, properties=properties)

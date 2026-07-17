"""Shared PostHog client initialized during Django application startup."""

from posthog import Posthog

client: Posthog

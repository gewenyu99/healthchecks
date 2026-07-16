# PostHog setup report

PostHog analytics, authenticated-user identification, exception tracking, event instrumentation, and a starter dashboard were added to the Django application.

## What was installed and initialized

- Added `posthog>=6.0,<7.0` to `requirements.txt`; build verification installed PostHog 6.9.1 successfully.
- Added environment-based `POSTHOG_PROJECT_TOKEN` and `POSTHOG_HOST` configuration, documented with placeholders in `.env.example`.
- Initialized an instance-based PostHog client in `hc/api/apps.py` during Django app startup, with exception autocapture enabled and shutdown registration.
- Installed `PosthogContextMiddleware` globally through Django settings.
- Authentication flows identify users with stable Django user IDs. Email is sent as a person property, not as event data. Identification covers password/magic-link authentication, WebAuthn, TOTP, remote-header SSO, administrator impersonation, and newly created accounts.

## Instrumented events

| Event | What it measures | File |
|---|---|---|
| `user_logged_in` | User completes password, magic-link, or two-factor authentication. | `hc/accounts/views.py` |
| `user_logged_out` | Authenticated user signs out. | `hc/accounts/views.py` |
| `account_signed_up` | A new account is created through the sign-up flow. | `hc/accounts/views.py` |
| `project_created` | Authenticated user creates a monitoring project. | `hc/accounts/views.py` |
| `check_created` | User creates a monitoring check in the web interface. | `hc/front/views.py` |
| `check_updated` | User saves a check name, slug, tags, or description. | `hc/front/views.py` |
| `check_paused` | User pauses an active monitoring check. | `hc/front/views.py` |
| `check_resumed` | User resumes a paused monitoring check. | `hc/front/views.py` |
| `check_deleted` | User removes a monitoring check. | `hc/front/views.py` |
| `check_copied` | User duplicates a monitoring check. | `hc/front/views.py` |
| `api_check_created` | API client creates a monitoring check. | `hc/api/views.py` |
| `api_check_updated` | API client updates a monitoring check. | `hc/api/views.py` |
| `api_check_deleted` | API client deletes a monitoring check. | `hc/api/views.py` |
| `api_check_paused` | API client pauses a monitoring check. | `hc/api/views.py` |
| `api_check_resumed` | API client resumes a paused monitoring check. | `hc/api/views.py` |

Capture calls use fresh PostHog contexts, stable authenticated IDs, and only non-PII check metadata.

## Identification

User identification was wired. Authenticated users are identified with their stable Django user ID at each authentication completion point, including returning authenticated flows. Email is attached to the person profile with `set()` rather than included in capture properties.

## Error tracking

Global uncaught exception tracking is enabled through `PosthogContextMiddleware` and `enable_exception_autocapture=True` on the initialized client. No per-view exception wrappers were added.

## Dashboard

A starter dashboard, **Analytics basics (wizard)**, was created with four tagged insights covering signups over time, signup-to-project-to-first-web-check activation, web versus API check creation, and web check lifecycle actions:

[Open the Analytics basics dashboard](https://us.posthog.com/project/228144/dashboard/1856777)

The MCP credential lacked `event_definition:read` and `property_definition:read`, so live event-schema validation was unavailable; dashboard and insight creation still succeeded using the recorded event inventory and verified payload shapes.

## Build conflicts and verification

Requirements installation succeeded, including `posthog 6.9.1`. `python manage.py check` passed, with the existing warning that `EMAIL_HOST` is unset (`hc.api.W002`). Standalone mypy, Ruff, and git verification commands were blocked by the execution environment and could not be run. CI should run `mypy --strict --show-traceback hc`. The MCP credential also lacks `event_definition:read` and `property_definition:read`, preventing live `read-data-schema` validation. These are the complete conflicts recorded during the run.

## Next steps

1. Set `POSTHOG_PROJECT_TOKEN` and `POSTHOG_HOST` in every deployment environment using the real project configuration, not only locally.
2. Run the full production build and test suite, then resolve any lint or type errors or fixture/mock updates surfaced by CI.
3. Exercise sign-in, signup, project creation, web checks, and API checks in a deployed environment and confirm the events and identified persons appear in PostHog.
4. Review the starter dashboard and extend it with product-specific breakdowns once event-definition read permissions are available.

## Before you merge

- [ ] Run a full production build and fix any lint or type errors introduced by the integration.
- [ ] Run the test suite; instrumented call sites may need updated mocks or fixtures.
- [ ] Confirm `POSTHOG_PROJECT_TOKEN` and `POSTHOG_HOST` are documented in `.env.example` and configured in deployment environments, not just locally.
- [ ] Confirm the returning-visitor authentication path also calls `identify`, so returning sessions do not fragment across anonymous IDs.

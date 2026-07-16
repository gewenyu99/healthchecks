# PostHog setup report

PostHog product analytics, user identification, global error tracking, and a starter dashboard were added to the Django application.

## What was installed and initialized

- Added `posthog>=6.0.0` to `requirements.txt`; the production dependency verification installed PostHog 7.23.0 successfully.
- Initialized an instance-based PostHog `Posthog` client from `hc.HealthchecksConfig` during Django startup.
- Configuration is environment-backed through `POSTHOG_PROJECT_TOKEN` and `POSTHOG_HOST`, documented in `.env.example` and configured locally in `.env`.
- Enabled SDK exception autocapture and registered SDK shutdown with `atexit` so queued events are flushed.
- Registered `posthog.integrations.django.PosthogContextMiddleware` for request context and exception forwarding.

## Events captured

| Event | What it measures | File |
|---|---|---|
| `account_registered` | A new account is created and sent its first login link. | `hc/accounts/views.py` |
| `user_logged_in` | A user completes password, WebAuthn, or TOTP authentication. | `hc/accounts/views.py` |
| `user_logged_out` | An authenticated user ends a session. | `hc/accounts/views.py` |
| `project_created` | A user creates a monitoring project. | `hc/accounts/views.py` |
| `team_member_invited` | A project manager successfully invites a team member. | `hc/accounts/views.py` |
| `check_created` | A user creates a monitoring check from the web interface. | `hc/front/views.py` |
| `check_updated` | A user updates a check's name, slug, tags, or description. | `hc/front/views.py` |
| `check_schedule_updated` | A user changes a check's schedule, timeout, grace period, or timezone. | `hc/front/views.py` |
| `check_paused` | A user pauses an active monitoring check. | `hc/front/views.py` |
| `check_resumed` | A user resumes a paused monitoring check. | `hc/front/views.py` |
| `check_deleted` | A user removes a monitoring check. | `hc/front/views.py` |
| `check_copied` | A user duplicates a monitoring check. | `hc/front/views.py` |
| `test_notification_sent` | A user successfully sends a test notification through a channel. | `hc/front/views.py` |
| `api_check_created` | An API client creates a monitoring check. | `hc/api/views.py` |

Event properties use safe metadata only; authenticated events use stable user IDs rather than personal data in event properties.

## User identification

Identification was wired through Django's `user_logged_in` signal in `hc/apps.py`. Successful password, magic-link, WebAuthn, TOTP, and remote-header authentication paths set PostHog person properties using the stable Django user ID and email. Logout reset was skipped because the instance-based Python SDK does not expose a corresponding session-reset API.

## Error tracking

Global error tracking is enabled through `enable_exception_autocapture=True` on the PostHog client and `PosthogContextMiddleware`, which captures request exceptions with context. No additional scattered exception handlers were needed.

## Dashboard

[Open the Analytics basics (wizard) dashboard](https://us.posthog.com/project/228144/dashboard/1856051)

The dashboard contains four wizard-tagged insights covering account activation, checks created by web/API, check lifecycle actions, and team invitations.

## Build conflict

Development dependency installation could not build `mysqlclient` because this environment lacks MySQL/MariaDB `pkg-config` metadata; type checking was therefore not run. Production requirements, including PostHog, installed successfully. The runtime also blocked direct mypy and Django management commands. No integration-caused errors were identified.

## Next steps

1. Set `POSTHOG_PROJECT_TOKEN` and `POSTHOG_HOST` in every deployment environment; do not rely only on the local `.env` file.
2. Run the application’s full production build and test suite in an environment with the required MySQL/MariaDB development metadata.
3. Exercise sign-up, authentication, project/team management, check lifecycle, notification, and API creation paths, then confirm the events appear in PostHog.
4. Review the dashboard after real traffic arrives and refine its insights or add product-specific breakdowns.

## Before you merge

- [ ] Run a full production build and fix any lint or type errors the generated code introduced.
- [ ] Run the test suite; instrumented call sites may need updated mocks or fixtures.
- [ ] Confirm `POSTHOG_PROJECT_TOKEN` and `POSTHOG_HOST` are documented in `.env.example` and set in deployment environments, not just locally.
- [ ] Because authentication identification was wired, verify that a returning authenticated visitor is identified so sessions do not fragment across anonymous IDs.

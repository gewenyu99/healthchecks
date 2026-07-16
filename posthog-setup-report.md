# PostHog setup report

PostHog product analytics, user identification, exception tracking, and a starter dashboard are configured for the Django application.

## Installed and initialized

- Added the `posthog` Python SDK to `requirements.txt` and installed it successfully; PostHog 7.23.0 is available.
- Initialized PostHog through Django `AppConfig.ready()` using the instance-based `Posthog` constructor.
- Configured `POSTHOG_PROJECT_TOKEN` and `POSTHOG_HOST` through the existing environment configuration pattern, with the required keys documented in `.env.example`.
- Registered `posthog.integrations.django.PosthogContextMiddleware` globally for request context and exception handling.
- Enabled SDK exception autocapture and registered shutdown handling with `atexit`.
- Runtime validation passed with `python manage.py check`; only the existing `EMAIL_HOST` configuration warning and the expected warning about missing process-environment PostHog keys were reported during that check.

## Events captured

| Event name | What it measures | Source file |
| --- | --- | --- |
| `user_logged_in` | An account successfully completes authentication. | `hc/accounts/views.py` |
| `user_logged_out` | An authenticated user ends their session. | `hc/accounts/views.py` |
| `account_created` | A new account is created through sign-up. | `hc/accounts/views.py` |
| `project_created` | A user creates a monitoring project. | `hc/accounts/views.py` |
| `check_created` | A user creates a new monitoring check. | `hc/front/views.py` |
| `check_updated` | A user saves check metadata or scheduling changes. | `hc/front/views.py` |
| `check_paused` | A user pauses an active monitoring check. | `hc/front/views.py` |
| `check_resumed` | A user resumes a paused monitoring check. | `hc/front/views.py` |
| `check_deleted` | A user deletes a monitoring check. | `hc/front/views.py` |
| `check_copied` | A user duplicates an existing monitoring check. | `hc/front/views.py` |
| `channel_assignment_updated` | A user enables or disables a notification channel for a check. | `hc/front/views.py` |
| `test_notification_sent` | A user sends a test notification through a channel. | `hc/front/views.py` |

Capture properties contain operational metadata only. Email is sent as a person property during identification, not as an event property.

## User identification

User identification is wired. Successful direct password or magic-link login, WebAuthn completion, and TOTP completion identify the authenticated user using the stable numeric Django user ID. The Python SDK's `set()` API is used for person properties, including email; the email is not included in captured event properties.

## Error tracking

Global error tracking is enabled through the registered `PosthogContextMiddleware` and SDK initialization with `enable_exception_autocapture=True`. No manual per-view exception capture calls were added.

## Dashboard

[Analytics basics (wizard)](https://us.posthog.com/project/228144/dashboard/1856639)

The dashboard contains four wizard-tagged insights covering account creation, account-to-first-check activation, monitoring checks created, and check lifecycle activity. The insights use the planned event names over a rolling 30-day range.

## Build conflict and verification limit

Development dependency installation was blocked by missing MySQL/MariaDB `pkg-config` development metadata: `mysqlclient` could not find the required MySQL/MariaDB development headers. Consequently, the repository's configured command `mypy --strict --show-traceback hc` could not be run. Use an environment with MySQL/MariaDB development headers, or the project's CI image, to install `requirements-dev.txt` and run that command.

The Django system check passed. The application does not automatically load the repository-root `.env` file, so deployment environments must export `POSTHOG_PROJECT_TOKEN` and `POSTHOG_HOST` as process environment variables. Running checks without those exported variables produces the SDK's empty-key warning; deployment must provide the real configured values.

## Next steps

1. Set `POSTHOG_PROJECT_TOKEN` and `POSTHOG_HOST` in every deployment environment, not only in the local `.env` file.
2. Run the full production build and test suite; update any mocks or fixtures affected by the instrumented authentication and monitoring views.
3. In a MySQL/MariaDB-enabled environment, install development requirements and run `mypy --strict --show-traceback hc`.
4. Exercise login, project creation, check lifecycle, channel assignment, and test notification flows, then confirm the events appear in the linked dashboard.

## Before you merge

- [ ] Run a full production build and fix any lint or type errors introduced by the integration.
- [ ] Run the test suite; instrumented call sites may need updated mocks or fixtures.
- [ ] Confirm the exact `POSTHOG_PROJECT_TOKEN` and `POSTHOG_HOST` names are documented in `.env.example` and set in deployment environments.
- [ ] Because authentication exists and identification is wired, verify the returning-visitor path also identifies users so returning sessions do not fragment across anonymous distinct IDs.

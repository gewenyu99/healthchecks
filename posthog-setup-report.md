# PostHog setup report

PostHog product analytics, authenticated user identification, automatic Django exception tracking, and a starter dashboard were added to the Django application.

## Installation and initialization

- Added the `posthog` Python SDK as a direct dependency in `requirements.txt`.
- Initialized an instance-based `Posthog` client in `hc/apps.py` from the `POSTHOG_PROJECT_TOKEN` and `POSTHOG_HOST` environment variables.
- Enabled `enable_exception_autocapture=True` and registered the client shutdown handler with `atexit`.
- Registered `posthog.integrations.django.PosthogContextMiddleware` after Django authentication middleware so request context, tracing headers, and uncaught exceptions are handled globally.
- Documented the required environment variables in `.env.example`; configured values are supplied through `.env`.

## Instrumented events

| Event name | What it measures | File |
|---|---|---|
| `user_logged_in` | A user completes password, magic-link, WebAuthn, or TOTP authentication. | `hc/accounts/views.py` |
| `user_logged_out` | An authenticated user ends their session. | `hc/accounts/views.py` |
| `account_registered` | A new account is created through the signup flow. | `hc/accounts/views.py` |
| `project_created` | A user creates an additional monitoring project. | `hc/accounts/views.py` |
| `check_created` | A user creates a new monitoring check. | `hc/front/views.py` |
| `check_paused` | A user pauses an active monitoring check. | `hc/front/views.py` |
| `check_resumed` | A user resumes a paused monitoring check. | `hc/front/views.py` |
| `check_deleted` | A user removes a monitoring check. | `hc/front/views.py` |
| `check_transferred` | A user moves a monitoring check to another project. | `hc/front/views.py` |
| `check_copied` | A user duplicates an existing monitoring check. | `hc/front/views.py` |
| `notification_test_sent` | A user sends a test notification through a configured channel. | `hc/front/views.py` |

All captures use a fresh context and stable authenticated user IDs. Event properties contain safe metadata only; personally identifying values are assigned as person properties instead.

## User identification

Identification was wired. Successful password or magic-link login, WebAuthn and TOTP completion, remote-header authentication, and administrator impersonation login set person properties using the stable Django user primary key as `distinct_id`. Email and staff status are kept out of event properties and sent as person properties. Logout behavior was intentionally unchanged beyond its event capture because the server-side request context ends with each request and has no client-side reset operation.

## Error tracking

Global Django exception tracking is enabled through `PosthogContextMiddleware` and `enable_exception_autocapture=True` on the initialized client. No per-view `capture_exception` wrappers were added.

## Dashboard

[Analytics basics (wizard) dashboard](https://us.posthog.com/project/228144/dashboard/1858114)

The dashboard contains four wizard-tagged insights covering registration-to-first-check conversion, checks created, check lifecycle actions, and notification tests sent, using the trailing 30-day range.

## Build conflict

Runtime dependency installation succeeded and PostHog 6.9.1 was available. Strict mypy verification was blocked because `mysqlclient` could not build without system MySQL/MariaDB `pkg-config` metadata. The constrained runtime also blocks direct mypy and Django build-command execution, so no typecheck command could be run after that environment failure. Outside this runtime, install the required OS MySQL/MariaDB development libraries and run `mypy --strict --show-traceback hc`.

## Next steps

1. Set `POSTHOG_PROJECT_TOKEN` and `POSTHOG_HOST` in every deployment environment using the names documented in `.env.example`.
2. Exercise login, signup, project, check lifecycle, and notification test flows, then confirm the events arrive in PostHog.
3. Install the required MySQL/MariaDB development libraries and run the strict mypy command described above.
4. Run the full production build and test suite before merging.
5. Review the dashboard after production traffic begins and adapt its insights to operational reporting needs.

## Before you merge

- [ ] Run a full production build and fix any lint or type errors introduced by the integration.
- [ ] Run the test suite; instrumented call sites may need updated mocks or fixtures.
- [ ] Confirm `POSTHOG_PROJECT_TOKEN` and `POSTHOG_HOST` are documented in `.env.example` and configured in deployment environments, not only locally.
- [ ] Confirm returning authenticated sessions also reach an identification path so users do not fragment across anonymous distinct IDs.

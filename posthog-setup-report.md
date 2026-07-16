# PostHog setup report

PostHog product analytics, authenticated user identification, automatic error tracking, and a starter dashboard are configured for the Django application.

## What was installed and initialized

- Added the unpinned `posthog` Python SDK dependency to `requirements.txt`; the dependency was installed successfully and PostHog 7.23.0 was available during validation.
- Added `POSTHOG_PROJECT_TOKEN` and `POSTHOG_HOST` configuration, documented in `.env.example`; the real values are kept in the local `.env` configuration rather than source code.
- Initialized the instance-based SDK from `hc/posthog/apps.py` through `PosthogConfig.ready()` using the environment-backed settings.
- Enabled `PosthogContextMiddleware` so request context and tracing headers are available to captured events.
- Enabled exception autocapture and registered SDK shutdown handling with `atexit`.
- Added context-based capture helpers using `new_context()` and `identify_context()` with stable authenticated Django user IDs.

## Events instrumented

| Event | What it measures | File |
|---|---|---|
| `user_logged_in` | A user successfully completes password, magic-link, or second-factor authentication. | `hc/accounts/views.py` |
| `user_logged_out` | An authenticated user explicitly signs out. | `hc/accounts/views.py` |
| `project_created` | A user creates an additional monitoring project. | `hc/accounts/views.py` |
| `check_created` | A user creates a monitoring check from the web interface. | `hc/front/views.py` |
| `check_configuration_updated` | A user saves a check name, tags, slug, or description change. | `hc/front/views.py` |
| `check_schedule_updated` | A user saves monitoring schedule or timeout settings. | `hc/front/views.py` |
| `check_paused` | A user pauses a monitoring check. | `hc/front/views.py` |
| `check_resumed` | A user resumes a paused monitoring check. | `hc/front/views.py` |
| `check_copied` | A user duplicates an existing monitoring check. | `hc/front/views.py` |
| `check_deleted` | A user removes a monitoring check. | `hc/front/views.py` |
| `notification_test_sent` | A user sends a test through a configured notification channel. | `hc/front/views.py` |
| `notification_channel_deleted` | A user removes a notification channel. | `hc/front/views.py` |

All custom event names use lower snake case. Capture properties avoid PII; email is stored as a person property during identification rather than as an event property.

## User identification

Identification was wired. New signups and successful password, magic-link, WebAuthn, and TOTP authentication flows update PostHog person properties using stable Django user IDs. Logout captures the event before session termination; no SDK reset is used because the server-side Python context is request-scoped and does not support a client-side session reset.

## Error tracking

Global error tracking is enabled through `PosthogContextMiddleware` and `enable_exception_autocapture=True` on the initialized SDK client. No additional route-level exception wrappers or manual capture calls were needed.

## Dashboard

[Open the Analytics basics dashboard](https://us.posthog.com/project/228144/dashboard/1856579)

The wizard-tagged dashboard includes four insights covering project-to-first-check activation, checks created over time, check lifecycle actions, and notification operations. The insights use the captured event names and a 30-day default date range.

## Build and validation conflict

Production dependency installation completed successfully. `python manage.py check` completed with the pre-existing `EMAIL_HOST` warning. Full development tooling validation could not be completed: installing `requirements-dev.txt` failed because `mysqlclient` could not locate a local MySQL/MariaDB `pkg-config` dependency, so the configured mypy workflow and lint tooling were not installed. Direct mypy and ruff invocations were unavailable. In addition, a direct local `manage.py check` invocation does not load the ignored `.env` automatically, so the SDK reported an empty API key in that shell; environment-key verification confirmed that `.env` contains both required PostHog keys. Run the full checks in an environment with the required database build dependencies and deployment environment variables configured.

## Next steps

1. Set `POSTHOG_PROJECT_TOKEN` and `POSTHOG_HOST` in every deployment environment using the names in `.env.example`.
2. Run the application through successful authentication, project/check management, and notification flows, then confirm the events appear in PostHog.
3. Review the dashboard and adjust date ranges, breakdowns, or insight definitions as product analytics needs evolve.
4. Run the full production build, tests, type checks, and lint checks in a development environment with MySQL/MariaDB build dependencies.

## Before you merge

- [ ] Run a full production build and fix any lint or type errors introduced by the integration.
- [ ] Run the test suite; instrumented call sites may need updated mocks or fixtures.
- [ ] Confirm `POSTHOG_PROJECT_TOKEN` and `POSTHOG_HOST` are present with their exact names in `.env.example` and configured in each deployment environment, not only locally.
- [ ] For authenticated returning visitors, verify the returning-session path also identifies the user so sessions do not fragment across anonymous distinct IDs.

# PostHog setup report

PostHog server-side analytics, user identification, automatic error tracking, and a starter dashboard are configured for the Django application.

## Installed and initialized

- Added `posthog==7.8.0` to `requirements.txt`.
- Configured the PostHog project token and host through environment-backed Django settings; the environment keys are documented in `docker/.env.example`.
- Initialized a single instance-based `Posthog` client from `hc.posthog.apps.PostHogConfig.ready()`.
- Enabled Django context middleware so request context and exceptions are handled globally.
- Enabled exception autocapture and registered client shutdown at process exit so queued events are flushed.
- Captures use the Django context pattern and stable authenticated user IDs. The pre-auth signup request is the only personless capture.

## Instrumented events

| Event name | What it measures | File |
|---|---|---|
| `user_logged_in` | A user completes password or magic-link authentication. | `hc/accounts/views.py` |
| `user_logged_out` | An authenticated user signs out. | `hc/accounts/views.py` |
| `account_signup_requested` | A valid signup request sends an instant login link. | `hc/accounts/views.py` |
| `project_created` | An authenticated user creates a monitoring project. | `hc/accounts/views.py` |
| `account_closed` | A user confirms account closure. | `hc/accounts/views.py` |
| `check_created` | An authenticated user creates a monitoring check in the web app. | `hc/front/views.py` |
| `check_paused` | An authenticated user pauses a monitoring check. | `hc/front/views.py` |
| `check_resumed` | An authenticated user resumes a monitoring check. | `hc/front/views.py` |
| `check_deleted` | An authenticated user deletes a monitoring check. | `hc/front/views.py` |
| `check_copied` | An authenticated user duplicates a monitoring check. | `hc/front/views.py` |
| `test_notification_sent` | An authenticated user successfully sends a test notification. | `hc/front/views.py` |
| `channel_deleted` | An authenticated user removes a notification channel. | `hc/front/views.py` |
| `api_check_created` | An API client creates a monitoring check. | `hc/api/views.py` |
| `api_check_deleted` | An API client deletes a monitoring check. | `hc/api/views.py` |

## User identification

Identification was wired. Successful password, magic-link, WebAuthn, and TOTP login paths update the PostHog person using the stable Django user ID as `distinct_id`; email is stored as a person property rather than an event property. Signup users are identified when their magic login link is redeemed through the shared successful-login flow. Logout reset was skipped because this is a server-side Python SDK integration using request contexts rather than a browser session identity.

## Error tracking

Global error tracking is covered by `PosthogContextMiddleware` and the instance client’s `enable_exception_autocapture=True` configuration. No additional handlers or scattered manual exception captures were added.

## Dashboard

[Analytics basics (wizard) dashboard](https://us.posthog.com/project/228144/dashboard/1856687)

The dashboard contains wizard-tagged insights for signup-to-project conversion, project-to-first-check conversion, monitoring setup activity, and check lifecycle activity over the last 30 days.

## Build conflicts and verification

The integration dependencies were installed successfully, including `posthog==7.8.0`. `python manage.py check` passed and reported only the existing `EMAIL_HOST`-unset warning. The project has no build, lint, or format scripts. Strict Mypy is configured in CI, but direct strict Mypy execution was disallowed by the execution harness. The full conflict is: `python manage.py check` reports only the existing `EMAIL_HOST`-unset warning; direct strict Mypy execution is disallowed by the harness.

## Next steps

1. Set the documented PostHog environment variables in every deployment environment, not only the local environment.
2. Run representative signup, login, project, check, channel, and API workflows in a deployed or staging environment.
3. Confirm the expected events and identified users appear in PostHog.
4. Run the project’s full production build and test suite in CI, including the configured strict Mypy check.
5. Use the starter dashboard to establish baseline conversion and monitoring lifecycle metrics.

## Before you merge

- [ ] Run a full production build and fix any lint or type errors introduced by the integration.
- [ ] Run the test suite; instrumented call sites may need updated mocks or fixtures.
- [ ] Confirm the exact PostHog environment variable names are documented in `.env.example` or bootstrap configuration and set in deployment environments, not just locally.
- [ ] Confirm returning authenticated sessions use the identified user path so events do not fragment onto anonymous distinct IDs.

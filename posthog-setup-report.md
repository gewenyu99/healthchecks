# PostHog setup report

PostHog product analytics, authenticated-user identification, automatic exception tracking, and a starter analytics dashboard are configured for the Django application.

## What was installed and initialized

- Added the `posthog` Python SDK to `requirements.txt` (validated as PostHog 6.9.1 during the build step).
- Configured `POSTHOG_PROJECT_TOKEN` and `POSTHOG_HOST` through environment-backed Django settings; the variable names are documented in `.env.example`.
- Registered `hc.posthog.PosthogConfig` and initialized an instance-based `Posthog` client from the Django app configuration using the environment settings.
- Enabled SDK exception autocapture and registered `posthog_client.shutdown` with `atexit` so events flush when the process exits.
- Registered Django's `posthog.integrations.django.PosthogContextMiddleware` for request context and tracing-header support.
- Instrumented events with the context API (`new_context()`, `identify_context()`, and `capture()`) using stable authenticated user IDs and non-PII event metadata.

## Events captured

| Event name | What it measures | File |
|---|---|---|
| `user_logged_in` | A user completes password or magic-link authentication. | `hc/accounts/views.py` |
| `user_logged_out` | An authenticated user signs out. | `hc/accounts/views.py` |
| `account_signed_up` | A new account is created through registration. | `hc/accounts/views.py` |
| `project_created` | An authenticated user creates an additional monitoring project. | `hc/accounts/views.py` |
| `team_member_invited` | A project manager successfully invites a team member. | `hc/accounts/views.py` |
| `account_closed` | A user confirms account closure. | `hc/accounts/views.py` |
| `check_created` | A user creates a monitoring check. | `hc/front/views.py` |
| `check_paused` | A user pauses a monitoring check. | `hc/front/views.py` |
| `check_resumed` | A user resumes a paused monitoring check. | `hc/front/views.py` |
| `check_deleted` | A user deletes a monitoring check. | `hc/front/views.py` |
| `notification_test_sent` | A user sends a test notification to a configured channel. | `hc/front/views.py` |
| `notification_channel_deleted` | A user deletes a notification channel. | `hc/front/views.py` |

## User identification

Identification was wired. Successful password or magic-link, WebAuthn, TOTP, remote-header, admin-initiated login, and signup paths update PostHog person properties using the stable Django user ID as `distinct_id`; email is sent as a person property via the instance client's `set()` method, not as event data. Logout does not reset a client-side session because this is a server-side integration without a client session to reset.

## Error tracking

Error tracking was already covered by the configured Django context middleware and the PostHog client’s `enable_exception_autocapture=True` setting. No additional global exception handler or manual wrapper was added.

## Dashboard

[Analytics basics (wizard)](https://us.posthog.com/project/228144/dashboard/1856752)

The dashboard includes tagged starter insights for account signups, signup-to-first-check activation, monitoring check lifecycle, and notification setup activity. No event data had been recorded when it was created.

## Build conflict

Type checking was blocked because `requirements-dev.txt` could not install the unrelated `mysqlclient` dependency without local MySQL/MariaDB development metadata. The direct `mypy` invocation was also unavailable before that installation. If type checking is needed in a suitable environment, install the system MySQL/MariaDB development libraries first, then install `requirements-dev.txt` and run `mypy --strict --show-traceback hc`.

## Next steps

1. Set `POSTHOG_PROJECT_TOKEN` and `POSTHOG_HOST` in every deployment environment using the names documented in `.env.example`.
2. Run the application through representative login, signup, project, check, and notification flows, then confirm the events appear in PostHog.
3. Review and extend the starter dashboard as product questions emerge.
4. Install the required MySQL/MariaDB development libraries and run strict mypy if type-check validation is required.

## Before you merge

- [ ] Run a full production build and fix any lint or type errors introduced by the integration.
- [ ] Run the test suite; instrumented call sites may need updated mocks or fixtures.
- [ ] Confirm the exact environment variable names are present in `.env.example` and set in deployment environments, not only locally.
- [ ] Confirm returning authenticated sessions also reach the identification path so users do not fragment onto anonymous distinct IDs.

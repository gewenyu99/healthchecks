# PostHog setup report

PostHog server-side analytics, user identification, automatic error tracking, and a starter dashboard were added to the Django application.

## Installed and initialized

- Added `posthog==6.9.1` to `requirements.txt`.
- Configured `POSTHOG_PROJECT_TOKEN` and `POSTHOG_HOST` through the project environment and documented both names in `.env.example`.
- Initialized an instance-based `Posthog` client from Django `ApiConfig.ready()` using settings-backed values.
- Enabled exception autocapture and registered client shutdown with `atexit`.
- Added `posthog.integrations.django.PosthogContextMiddleware` for request context and tracing headers.

## Instrumented events

| Event | What it measures | File |
|---|---|---|
| `account_created` | A new account is created through signup. | `hc/accounts/views.py` |
| `project_created` | An authenticated user creates a monitoring project. | `hc/accounts/views.py` |
| `project_key_created` | A project API or ping key is generated. | `hc/accounts/views.py` |
| `team_member_invited` | A manager successfully invites a team member. | `hc/accounts/views.py` |
| `project_name_updated` | A project name change is saved. | `hc/accounts/views.py` |
| `project_transfer_initiated` | A project owner initiates a transfer request. | `hc/accounts/views.py` |
| `project_ownership_transferred` | A pending project transfer is accepted. | `hc/accounts/views.py` |
| `password_changed` | An authenticated user successfully changes a password. | `hc/accounts/views.py` |
| `two_factor_enabled` | An authenticated user enables TOTP two-factor authentication. | `hc/accounts/views.py` |
| `two_factor_disabled` | An authenticated user disables TOTP two-factor authentication. | `hc/accounts/views.py` |
| `account_closed` | An authenticated user closes an account. | `hc/accounts/views.py` |
| `check_created` | A user creates a monitoring check. | `hc/front/views.py` |
| `check_paused` | A user pauses a monitoring check. | `hc/front/views.py` |
| `check_resumed` | A user resumes a monitoring check. | `hc/front/views.py` |
| `test_notification_sent` | A user sends a test notification through a channel. | `hc/front/views.py` |

## User identification

Identification was wired. Authenticated users use their stable Django primary key as the distinct ID across signup and password/token, WebAuthn, TOTP, remote-header, and admin impersonation authentication paths. Email is sent as a person property via `set()`, not as an event property. There is no browser SDK, so logout remains Django session logout without a client-side reset.

## Error tracking

Automatic error tracking is enabled globally through `enable_exception_autocapture=True` on the initialized PostHog client and `PosthogContextMiddleware`. No manual per-view exception instrumentation was needed.

## Dashboard

[Analytics basics (wizard)](https://us.posthog.com/project/228144/dashboard/1856727) includes four tagged insights covering account-to-first-check activation, daily check creation, project setup activity, and check pause/resume activity.

## Build conflicts and verification

Requirements installed successfully, including `posthog==6.9.1`. `python manage.py check` passed with the pre-existing `hc.api.W002` warning because `EMAIL_HOST` is unset. Direct `mypy --strict --show-traceback hc` verification could not run because the execution harness blocks that command; no source changes were required for this conflict. The repository has no package-manager manifest or package scripts.

## Next steps

1. Set `POSTHOG_PROJECT_TOKEN` and `POSTHOG_HOST` in every deployment environment, not only locally.
2. Run the application through signup, authentication, project, security, and check workflows and confirm events arrive in PostHog.
3. Review the starter dashboard and adjust filters or insight definitions for production reporting needs.
4. Configure `EMAIL_HOST` if email functionality is required, then rerun Django checks.
5. Run the production build and type checks in CI where the normal project tooling is available.

## Before you merge

- [ ] Run a full production build and fix any lint or type errors introduced by the integration.
- [ ] Run the test suite and update mocks or fixtures for instrumented call sites if needed.
- [ ] Confirm `POSTHOG_PROJECT_TOKEN` and `POSTHOG_HOST` are documented in `.env.example` and set in deployment environments.
- [ ] Exercise the returning-visitor authentication path and confirm it also identifies users, preventing anonymous distinct-ID fragmentation.

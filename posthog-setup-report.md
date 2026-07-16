# PostHog setup report

PostHog product analytics, user identification, and automatic exception tracking were added to the Django application, with a starter dashboard for the captured product events.

## What was installed and initialized

- Added the PostHog Python SDK to `requirements.txt` with `posthog>=6.0,<7.0`; production requirements installed successfully, including PostHog 6.9.3.
- Added `POSTHOG_PROJECT_TOKEN` and `POSTHOG_HOST` settings, documented the keys in `.env.example`, and configured the local environment.
- Registered `hc.posthog.apps.PosthogConfig` and `posthog.integrations.django.PosthogContextMiddleware`.
- Initialized the SDK once from the Django app configuration using the instance-based `Posthog()` API, environment-backed settings, exception autocapture, and an `atexit` shutdown hook.
- Instrumented server-side captures with the Django/PostHog context API in `hc/accounts/views.py` and `hc/front/views.py`.

## Events captured

| Event name | What it measures | File |
|---|---|---|
| `user_signed_up` | A new account is created and a sign-in link is sent. | `hc/accounts/views.py` |
| `user_logged_in` | A user completes password, magic-link, WebAuthn, or TOTP authentication. | `hc/accounts/views.py` |
| `user_logged_out` | An authenticated user signs out. | `hc/accounts/views.py` |
| `project_created` | An authenticated user creates an additional monitoring project. | `hc/accounts/views.py` |
| `check_created` | A monitoring check is successfully created from the web application. | `hc/front/views.py` |
| `check_updated` | A check's name, tags, description, or schedule configuration is changed. | `hc/front/views.py` |
| `check_paused` | An active monitoring check is paused. | `hc/front/views.py` |
| `check_resumed` | A paused monitoring check is resumed. | `hc/front/views.py` |
| `check_deleted` | A monitoring check is removed. | `hc/front/views.py` |
| `check_copied` | A monitoring check is duplicated within a project. | `hc/front/views.py` |
| `check_transferred` | A monitoring check is moved to another project. | `hc/front/views.py` |
| `test_notification_sent` | A user sends a test notification through a configured channel. | `hc/front/views.py` |

## User identification

User identification was wired through Django's `user_logged_in` signal in `hc/posthog/apps.py`. It identifies authenticated users with their stable Django primary key and stores email as a person property rather than an event property. The signal covers password, magic-link, WebAuthn, TOTP, and remote-header login paths. No login view changes are required.

## Error tracking

Error tracking was already satisfied by the registered `PosthogContextMiddleware` together with `enable_exception_autocapture=True` in the shared SDK initialization. This provides the global uncaught-exception capture boundary without scattered manual exception captures.

## Dashboard

[Analytics basics (wizard)](https://us.posthog.com/project/228144/dashboard/1858407)

The dashboard contains five saved insights covering account-to-project conversion, login-to-first-check activation, checks created, check lifecycle health, and test notification deliveries.

## Build conflict

Full development dependency installation is blocked by missing local MySQL/MariaDB development libraries: installing `requirements-dev.txt` stops at `mysqlclient` because the required local MySQL/MariaDB `pkg-config` development files are unavailable. This prevented CI-equivalent full repository typechecking. Production requirements installation completed successfully, and the conflict is environmental and unrelated to the PostHog integration.

## Next steps

1. Set `POSTHOG_PROJECT_TOKEN` and `POSTHOG_HOST` in every deployment environment using the values appropriate for the PostHog project.
2. Exercise signup, login, project creation, check lifecycle, transfer/copy, and test-notification flows, then confirm events and identified users in PostHog.
3. Run the full production build and test suite in CI or an environment with the required MySQL/MariaDB development libraries.
4. Review the starter dashboard and adjust insight filters or breakdowns to match operational reporting needs.

## Before you merge

- [ ] Run a full production build and fix any lint or type errors introduced by the generated instrumentation.
- [ ] Run the test suite; instrumented call sites may need updated mocks or fixtures.
- [ ] Confirm `POSTHOG_PROJECT_TOKEN` and `POSTHOG_HOST` are documented with their exact names in `.env.example` and configured in deployment environments, not only locally.
- [ ] Confirm the returning-visitor path also calls `identify`, so returning authenticated sessions do not fragment onto anonymous distinct IDs.

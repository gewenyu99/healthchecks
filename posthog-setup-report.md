# PostHog setup report

PostHog product analytics and Django error tracking were integrated with environment-backed configuration, authenticated user identification, 14 product events, and a starter dashboard.

## Installed and initialized

- Added `posthog==7.9.7` to `requirements.txt`; the main requirements installation completed successfully.
- Configured `POSTHOG_PROJECT_TOKEN` and `POSTHOG_HOST` through the project environment and documented the keys in `.env.example`.
- Django settings read the PostHog configuration from environment variables.
- Added `posthog.integrations.django.PosthogContextMiddleware` for request context and tracing headers.
- Initialized an instance-based `Posthog` client in `hc/api/apps.py` with `enable_exception_autocapture=True` and registered shutdown with `atexit`.

## Events captured

| Event | What it measures | File |
|---|---|---|
| `account_logged_in` | A user successfully completes authentication. | `hc/accounts/views.py` |
| `account_logged_out` | An authenticated user signs out. | `hc/accounts/views.py` |
| `account_created` | A new account is created during sign-up. | `hc/accounts/views.py` |
| `project_created` | An authenticated user creates a project. | `hc/accounts/views.py` |
| `project_name_updated` | A project name is successfully changed. | `hc/accounts/views.py` |
| `check_created` | A monitoring check is created from the web interface. | `hc/front/views.py` |
| `check_updated` | A monitoring check name, slug, tags, or description is saved. | `hc/front/views.py` |
| `check_schedule_updated` | A monitoring check schedule or timeout is saved. | `hc/front/views.py` |
| `check_paused` | A monitoring check is paused. | `hc/front/views.py` |
| `check_resumed` | A monitoring check is resumed. | `hc/front/views.py` |
| `check_deleted` | A monitoring check is removed. | `hc/front/views.py` |
| `check_copied` | A monitoring check is duplicated. | `hc/front/views.py` |
| `notification_test_sent` | A user sends a test notification through a channel. | `hc/front/views.py` |
| `notification_channel_deleted` | A notification channel is removed. | `hc/front/views.py` |

## User identification

Identification was wired. Successful direct login, signup account creation, WebAuthn completion, and TOTP completion set PostHog person properties using the stable Django user ID as the distinct ID. Email is sent as a person property rather than an event property. Logout captures the event before session termination; no browser-session reset was added because the server-side SDK has no corresponding operation.

## Error tracking

Global Django exception tracking is enabled through `PosthogContextMiddleware` and the SDK client’s `enable_exception_autocapture=True` setting. No additional per-route exception instrumentation was required.

## Dashboard

[Open the Analytics basics dashboard](https://us.posthog.com/project/228144/dashboard/1858142)

The wizard-tagged dashboard contains four insights: an account activation funnel, account activity, monitoring check lifecycle, and notification channel activity. The newly instrumented events had no recorded activity during validation and will populate as the application emits them.

## Build conflict

The main `requirements.txt` installation succeeded, including `posthog==7.9.7`. Full development dependency installation could not complete because `mysqlclient==2.2.8` requires MySQL/MariaDB development metadata, and the environment lacks the required `pkg-config` configuration. The repository’s strict mypy verification command (`mypy --strict --show-traceback hc`) could not be executed because direct mypy commands are blocked by the harness. No integration-specific build failure was found. Once the environment provides MySQL/MariaDB development packages and permits the typecheck command, run `pip install -r requirements-dev.txt` followed by `mypy --strict --show-traceback hc`.

## Next steps

1. Set `POSTHOG_PROJECT_TOKEN` and `POSTHOG_HOST` in every deployment environment, not only local development.
2. Deploy or run the application and exercise login, project, check, and notification workflows so events begin populating.
3. Review the dashboard after real traffic arrives and adjust insight date ranges or breakdowns as needed.
4. Provision MySQL/MariaDB development metadata and run the full development dependency install and strict mypy check.
5. Run the application test suite and production build before merging.

## Before you merge

- [ ] Run a full production build and fix any lint or type errors introduced by the integration.
- [ ] Run the test suite; instrumented call sites may need updated mocks or fixtures.
- [ ] Confirm `POSTHOG_PROJECT_TOKEN` and `POSTHOG_HOST` are documented with their exact names in `.env.example` and set in deployment environments.
- [ ] Confirm the returning-visitor authentication path calls identify so authenticated events do not fragment onto anonymous distinct IDs.

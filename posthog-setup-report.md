# PostHog setup report

PostHog server-side analytics, user identification, exception tracking, and a starter analytics dashboard are configured for the Django application.

## What was installed and initialized

- Added the `posthog` Python SDK to `requirements.txt`; dependency installation completed successfully, with `posthog 6.9.3` already satisfied.
- Added `POSTHOG_PROJECT_TOKEN` and `POSTHOG_HOST` configuration through the environment and documented the keys in `.env.example`.
- Added settings-backed PostHog configuration and registered `posthog.integrations.django.PosthogContextMiddleware` globally.
- Initialized an instance-based `Posthog` client from `ApiConfig.ready()` using environment-backed settings, with `enable_exception_autocapture=True` and an `atexit` shutdown handler to flush events.
- Django verification passed with `python manage.py check`. It reported only the pre-existing `hc.api.W002` warning that `EMAIL_HOST` is unset.

## Events instrumented

| Event | What it measures | File |
|---|---|---|
| `account_signup_completed` | A new account is created through the signup flow. | `hc/accounts/views.py` |
| `user_logged_in` | A user completes authentication. | `hc/accounts/views.py` |
| `user_logged_out` | An authenticated user signs out. | `hc/accounts/views.py` |
| `project_created` | An authenticated user creates a monitoring project. | `hc/accounts/views.py` |
| `account_closed` | A user confirms permanent account closure. | `hc/accounts/views.py` |
| `check_created` | A user creates a new monitoring check. | `hc/front/views.py` |
| `check_paused` | A user pauses a monitoring check. | `hc/front/views.py` |
| `check_resumed` | A user resumes a paused monitoring check. | `hc/front/views.py` |
| `check_deleted` | A user deletes a monitoring check. | `hc/front/views.py` |
| `check_copied` | A user duplicates an existing monitoring check. | `hc/front/views.py` |

Events use snake_case names, authenticated stable distinct IDs, and no PII in event properties.

## User identification

User identification was wired. Successful direct password or magic-link login, WebAuthn and TOTP completion, remote-header authentication, admin impersonation login, and newly created signups update the PostHog person using `str(user.pk)` as the stable distinct ID. Email is stored as a person property through the instance client's `set()` API, not as an event property. The Python SDK instance API does not expose `identify()`, so `set()` is used for these person updates.

## Error tracking

Global Django exception tracking is enabled by the registered `PosthogContextMiddleware` and the initialized PostHog client’s `enable_exception_autocapture=True` setting. No per-view exception wrappers were needed.

## Dashboard

[Open the Analytics basics dashboard](https://us.posthog.com/project/228144/dashboard/1858364).

The wizard-tagged dashboard contains five insights covering signup-to-project conversion, project-to-first-check conversion, account signup trends, check lifecycle activity, and authentication activity. The insights currently have no results because application events have not yet been ingested.

## Build conflict

`ruff check hc` could not run because the runtime command allowlist blocked the `ruff` command. The Django check otherwise passed with only the existing `EMAIL_HOST` warning, which is unrelated to this integration. Run the lint command in a normal development shell if required.

## Next steps

1. Set `POSTHOG_PROJECT_TOKEN` and `POSTHOG_HOST` in every deployment environment, using `.env.example` for the exact variable names; do not rely only on the local `.env` file.
2. Deploy or run the application and exercise signup, authentication, project, account, and check lifecycle paths.
3. Confirm the ten events and identified users appear in PostHog, then review the dashboard as data arrives.
4. Run the full production build and test suite, and run `ruff check hc` in a normal development environment.
5. Address the unrelated `EMAIL_HOST` configuration warning if the deployment requires outbound email.

## Before you merge

- [ ] Run a full production build and fix any lint or type errors introduced by the integration.
- [ ] Run the test suite; instrumented call sites may need updated mocks or fixtures.
- [ ] Confirm `POSTHOG_PROJECT_TOKEN` and `POSTHOG_HOST` are set in deploy environments and documented in `.env.example`.
- [ ] Confirm returning authenticated sessions continue using the identified user distinct ID rather than fragmenting onto anonymous IDs.

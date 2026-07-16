# PostHog setup report

PostHog product analytics, user identification, automatic error tracking, and a starter analytics dashboard are configured for the Django application.

## What was installed and initialized

- Added `posthog>=6.0.0,<7.0.0` to `requirements.txt`; the build installed PostHog 6.9.3 successfully.
- Added Django startup initialization in `hc/apps.py` using the instance-based `Posthog()` client, configured from `POSTHOG_PROJECT_TOKEN` and `POSTHOG_HOST` settings.
- Enabled `enable_exception_autocapture=True` and registered client shutdown with `atexit`.
- Added `posthog.integrations.django.PosthogContextMiddleware` to provide request context and the global exception boundary.
- Added the PostHog settings and environment documentation in `hc/settings.py` and `.env.example`; local environment values are configured through `.env`.

## Events captured

| Event name | What it measures | File |
| --- | --- | --- |
| `user_logged_in` | A user completes authentication and starts a session. | `hc/accounts/views.py` |
| `user_logged_out` | An authenticated user ends their session. | `hc/accounts/views.py` |
| `account_signup_requested` | A new account sign-up request is accepted and a login link is sent. | `hc/accounts/views.py` |
| `project_created` | An authenticated user creates a monitoring project. | `hc/accounts/views.py` |
| `project_deleted` | An owner deletes a monitoring project. | `hc/accounts/views.py` |
| `check_created` | An authenticated user creates a monitoring check. | `hc/front/views.py` |
| `check_paused` | An authenticated user pauses an active monitoring check. | `hc/front/views.py` |
| `check_resumed` | An authenticated user resumes a paused monitoring check. | `hc/front/views.py` |
| `check_deleted` | An authenticated user removes a monitoring check. | `hc/front/views.py` |
| `check_copied` | An authenticated user duplicates a monitoring check. | `hc/front/views.py` |
| `test_notification_sent` | An authenticated user successfully sends a test notification. | `hc/front/views.py` |
| `channel_deleted` | An authenticated user removes a notification channel. | `hc/front/views.py` |

## User identification

User identification was wired. Authentication and account flows use each user's database primary key (`str(user.pk)`) as the stable distinct ID. Email is sent only as a person property through `set()`, not as an event property. Coverage includes account creation, password and magic-link authentication, both 2FA login methods, header-based authentication, and administrator impersonation login. Event captures use fresh contexts and authenticated IDs.

## Error tracking

Error tracking did not require additional edits: PostHog initialization enables `enable_exception_autocapture=True`, and `PosthogContextMiddleware` is registered as Django's global exception boundary.

## Dashboard

[Open the Analytics basics dashboard](https://us.posthog.com/project/228144/dashboard/1858320). It contains four starter insights: Signup requests, Signup to project creation, Monitoring check lifecycle, and Test notifications sent, using the recorded event names over the last 30 days.

## Build conflict

Strict mypy verification could not run because the execution harness disallows direct mypy commands. The dependency installation succeeded, and `python manage.py check` passed with only the existing warning that `EMAIL_HOST` is unset. No integration-specific type errors were observed during review.

## Next steps

1. Set `POSTHOG_PROJECT_TOKEN` and `POSTHOG_HOST` in every deployment environment, using `.env.example` as the key reference; do not rely on local `.env` values in production.
2. Exercise the authentication, signup, project, check, and notification flows in a staging environment and confirm the events appear in PostHog.
3. Review the starter dashboard and add product-specific breakdowns or alerts as needed.
4. Run the full production build, test suite, and the repository's lint/type checks in CI.

## Before you merge

- [ ] Run a full production build and fix any lint or type errors introduced by the integration.
- [ ] Run the test suite; instrumented call sites may need updated mocks or fixtures.
- [ ] Confirm `POSTHOG_PROJECT_TOKEN` and `POSTHOG_HOST` are documented with their exact names and set in deployment environments, not only locally.
- [ ] Because authentication identification was wired, verify that returning authenticated visitors also call identification so sessions do not fragment across anonymous IDs.

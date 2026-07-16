<wizard-report>
# PostHog post-wizard report

The wizard has completed a deep integration of PostHog analytics into the Healthchecks Django application. PostHog is now initialized via `hc/api/apps.py` using the `ApiConfig.ready()` hook, with the `PosthogContextMiddleware` added to capture session and request context across all views. User identity and key business events are tracked server-side across the accounts and front modules.

| Event Name | Description | File |
|---|---|---|
| `user_signed_up` | A new user account was created via the signup form | `hc/accounts/views.py` |
| `user_logged_in` | A user successfully authenticated and logged in | `hc/accounts/views.py` |
| `user_logged_out` | A user logged out of their account | `hc/accounts/views.py` |
| `check_created` | A new health check was created in a project | `hc/front/views.py` |
| `check_deleted` | A health check was deleted from a project | `hc/front/views.py` |
| `check_timeout_updated` | A health check's schedule or timeout settings were updated | `hc/front/views.py` |
| `project_created` | A new project was created by a user | `hc/accounts/views.py` |
| `project_removed` | A project and all its checks were permanently deleted | `hc/accounts/views.py` |
| `team_member_invited` | A team member was invited to collaborate on a project | `hc/accounts/views.py` |
| `account_closed` | A user permanently closed their account | `hc/accounts/views.py` |
| `2fa_enabled` | A user enabled two-factor authentication via TOTP | `hc/accounts/views.py` |

## Next steps

We've built some insights and a dashboard for you to keep an eye on user behavior, based on the events we just instrumented:

- **Dashboard**: [Analytics basics (wizard)](https://us.posthog.com/project/228144/dashboard/1856071)
- **Insight**: [User signups over time](https://us.posthog.com/project/228144/insights/COckPc2x)
- **Insight**: [Signup to login conversion funnel](https://us.posthog.com/project/228144/insights/XaO7czOH)
- **Insight**: [New checks created over time](https://us.posthog.com/project/228144/insights/Jtru5HnG)
- **Insight**: [Account churn (closures) over time](https://us.posthog.com/project/228144/insights/6a6sq79Q)
- **Insight**: [Team growth: invitations sent](https://us.posthog.com/project/228144/insights/jtIUUxkA)

## Verify before merging

- [ ] Run a full production build (the wizard only verified the files it touched) and fix any lint or type errors introduced by the generated code.
- [ ] Run the test suite — call sites that were rewritten or instrumented may need updated mocks or fixtures.
- [ ] Add `POSTHOG_PROJECT_TOKEN` and `POSTHOG_HOST` to `.env.example` and any bootstrap scripts so collaborators know what to set.
- [ ] Confirm the returning-visitor path also calls `identify` — a handler that only identifies on fresh login can leave returning sessions on anonymous distinct IDs. The `check_token` (magic link) login flow also triggers `_check_2fa` which fires `user_logged_in` with identify — confirm this covers all your login paths.

### Agent skill

We've left an agent skill folder in your project. You can use this context for further agent development when using Claude Code. This will help ensure the model provides the most up-to-date approaches for integrating PostHog.

</wizard-report>

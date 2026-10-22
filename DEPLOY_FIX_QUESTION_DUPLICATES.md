# Railway duplicate Question fix

This version fixes Railway deploy crash:

```text
olympiad.models.Question.MultipleObjectsReturned: get() returned more than one Question
```

Changes:
- `seed_demo.py` no longer uses `Question.objects.get_or_create(...)` for seeded questions.
- It now uses `filter(...).first()` and updates the first matching question, so old duplicate questions in PostgreSQL will not crash the deploy.
- `start_railway.sh` no longer stops the whole Railway app if `seed_demo` prints a warning later; migrate and gunicorn still run.
- `railway.json` has no healthcheck path, so Railway will not fail because of healthcheck routing.

After pushing this version to GitHub, Railway should redeploy successfully.

from django.db import migrations

GRADES = [f'{n}-sinf' for n in range(1, 12)]


def clear_short_math_levels(apps, schema_editor):
    # 0028 may have loaded only 20 questions per grade; drop those so seed_demo loads all 25.
    Level = apps.get_model('olympiad', 'Level')
    Question = apps.get_model('olympiad', 'Question')
    for level in Level.objects.filter(subject__name='Matematika', name__in=GRADES):
        qs = Question.objects.filter(level=level)
        if 0 < qs.count() < 25:
            qs.delete()


class Migration(migrations.Migration):
    dependencies = [('olympiad', '0028_math_1_11_new_tests')]
    operations = [migrations.RunPython(clear_short_math_levels, migrations.RunPython.noop)]

from django.db import migrations

OLD_LEVELS = {
    'Matematika': ['0-sinf'],
    'English': ['Pre-Intermediate'],
    'Arab tili': ['A1', 'A2'],
    'Rus tili': ['Pochemuchka'],
}


def remove_old_empty_levels(apps, schema_editor):
    # Eski testlardan qolgan, endi savoli yo'q darajalarni olib tashlaydi.
    # O'quvchisi bor daraja yoki fanga tegilmaydi.
    Subject = apps.get_model('olympiad', 'Subject')
    Level = apps.get_model('olympiad', 'Level')
    for subject_name, level_names in OLD_LEVELS.items():
        Level.objects.filter(
            subject__name=subject_name,
            name__in=level_names,
            students__isnull=True,
            questions__isnull=True,
        ).delete()
    Subject.objects.filter(
        name__in=['Arab tili'],
        levels__isnull=True,
        students__isnull=True,
    ).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('olympiad', '0020_question_image_url'),
    ]

    operations = [
        migrations.RunPython(remove_old_empty_levels, migrations.RunPython.noop),
    ]

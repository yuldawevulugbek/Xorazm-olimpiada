from django.db import migrations

# Antalya olimpiadasida faqat shu fan va darajalar qoladi (tests_data.py bilan bir xil).
KEEP = {
    'Matematika': ['Kids', '1-sinf', '2-sinf', '3-sinf', '4-sinf', '5-sinf', '6-sinf', '7-sinf', '8-sinf', '10-sinf', '11-sinf'],
    'IT': ['HTML CSS', 'JavaScript', 'React', 'Vue', 'Python'],
    'Kompyuter': ['Excel', 'Word Excel PowerPoint'],
}


def replace_with_antalya_tests(apps, schema_editor):
    # Eski savollarning hammasi o'chiriladi, seed_demo yangi testlarni yuklaydi.
    # O'quvchisi bor daraja va fanlarga tegilmaydi, faqat bo'sh qolganlari tozalanadi.
    Subject = apps.get_model('olympiad', 'Subject')
    Level = apps.get_model('olympiad', 'Level')
    Question = apps.get_model('olympiad', 'Question')
    Question.objects.all().delete()
    for level in Level.objects.select_related('subject').filter(students__isnull=True):
        if level.name not in KEEP.get(level.subject.name, []):
            level.delete()
    Subject.objects.filter(levels__isnull=True, students__isnull=True).exclude(name__in=KEEP).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('olympiad', '0024_remove_mental_subject'),
    ]

    operations = [
        migrations.RunPython(replace_with_antalya_tests, migrations.RunPython.noop),
    ]

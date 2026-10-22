from django.db import migrations


def noop(apps, schema_editor):
    # Test/daraja seedlari olib tashlandi. Faqat Mental arifmetika qoldiriladi.
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('olympiad', '0006_question_version_student_selected_version'),
    ]

    operations = [
        migrations.RunPython(noop, migrations.RunPython.noop),
    ]

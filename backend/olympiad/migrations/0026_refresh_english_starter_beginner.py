from django.db import migrations


def clear_starter_and_beginner(apps, schema_editor):
    """English Starter (30 ta rasmli test) va Beginner (20 ta test, 8–13 rasmli) yangilandi.

    Eski savollar o'chiriladi; yangilarini deploy paytida seed_demo (tests_loader.load_tests)
    tests_data.py dan bo'sh darajalarga yozadi.
    """
    Question = apps.get_model('olympiad', 'Question')
    Question.objects.filter(
        subject__name__iexact='English',
        level__name__in=['Starter', 'Beginner'],
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('olympiad', '0025_refresh_english_elementary_intermediate'),
    ]

    operations = [
        migrations.RunPython(clear_starter_and_beginner, migrations.RunPython.noop),
    ]

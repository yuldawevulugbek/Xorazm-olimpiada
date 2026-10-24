from django.db import migrations


def clear_old_english_questions(apps, schema_editor):
    """English Elementary va Intermediate savollari darajasiga mos yangilari bilan almashtiriladi.

    Bu yerda faqat eski savollar o'chiriladi; yangilarini deploy paytida seed_demo
    (tests_loader.load_tests) bo'sh darajalarga yozadi.
    """
    Question = apps.get_model('olympiad', 'Question')
    Question.objects.filter(
        subject__name__iexact='English',
        level__name__in=['Elementary', 'Intermediate'],
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('olympiad', '0024_remove_mental_subject'),
    ]

    operations = [
        migrations.RunPython(clear_old_english_questions, migrations.RunPython.noop),
    ]

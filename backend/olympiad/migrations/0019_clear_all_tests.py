from django.db import migrations


def clear_all_tests(apps, schema_editor):
    # Barcha eski test savollarini o'chiradi. Fanlar, darajalar va o'quvchilar qoladi.
    Question = apps.get_model('olympiad', 'Question')
    Question.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ('olympiad', '0018_add_rus_tili_tests'),
    ]

    operations = [
        migrations.RunPython(clear_all_tests, migrations.RunPython.noop),
    ]

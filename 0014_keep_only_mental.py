from django.db import migrations


def keep_only_mental(apps, schema_editor):
    Subject = apps.get_model('olympiad', 'Subject')
    Level = apps.get_model('olympiad', 'Level')
    Question = apps.get_model('olympiad', 'Question')

    mental_subject, _ = Subject.objects.get_or_create(name='Mental arifmetika')
    mental_level, _ = Level.objects.get_or_create(subject=mental_subject, name='Mental A', defaults={'duration_minutes': 5})
    mental_level.duration_minutes = 5
    mental_level.save(update_fields=['duration_minutes'])

    Question.objects.exclude(subject=mental_subject).delete()
    Level.objects.exclude(id=mental_level.id).delete()
    Subject.objects.exclude(name='Mental arifmetika').delete()


class Migration(migrations.Migration):
    dependencies = [
        ('olympiad', '0013_clear_existing_branches'),
    ]

    operations = [
        migrations.RunPython(keep_only_mental, migrations.RunPython.noop),
    ]

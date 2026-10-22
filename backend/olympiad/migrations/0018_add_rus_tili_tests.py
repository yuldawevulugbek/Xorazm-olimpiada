from django.db import migrations


def add_rus_tili_tests(apps, schema_editor):
    Subject = apps.get_model('olympiad', 'Subject')
    Level = apps.get_model('olympiad', 'Level')
    Question = apps.get_model('olympiad', 'Question')
    RUS_TESTS = []  # eski testlar o'chirildi

    subject, _ = Subject.objects.get_or_create(name='Rus tili')
    for level_name, questions in RUS_TESTS:
        level, _ = Level.objects.get_or_create(
            subject=subject,
            name=level_name,
            defaults={'duration_minutes': 60},
        )
        level.duration_minutes = 60
        level.save(update_fields=['duration_minutes'])
        Question.objects.filter(subject=subject, level=level).delete()
        Question.objects.bulk_create([
            Question(
                subject=subject,
                level=level,
                version=1,
                text=item['text'],
                option_a=item['option_a'],
                option_b=item['option_b'],
                option_c=item['option_c'],
                option_d=item['option_d'],
                correct_answer=item['correct_answer'],
            )
            for item in questions
        ])


def remove_rus_tili_tests(apps, schema_editor):
    Subject = apps.get_model('olympiad', 'Subject')
    Subject.objects.filter(name='Rus tili').delete()


class Migration(migrations.Migration):
    dependencies = [
        ('olympiad', '0017_add_arab_tili_tests'),
    ]

    operations = [
        migrations.RunPython(add_rus_tili_tests, remove_rus_tili_tests),
    ]

# 2026-10-24: Matematika Kids (takroriy "4 * 5" savoli almashtirildi), Matematika 10-sinf, IT JavaScript, IT React
# va Kompyuter Word Excel PowerPoint savollarida to'g'ri javob harflari A/B/C/D bo'yicha teng taqsimlandi.
# Savollar o'chirilmaydi (natijalar saqlanib qoladi): bazadagi savollar tests_data.py bo'yicha joyida yangilanadi.
from django.db import migrations

LEVELS = [
    ('Matematika', 'Kids'),
    ('Matematika', '10-sinf'),
    ('IT', 'JavaScript'),
    ('IT', 'React'),
    ('Kompyuter', 'Word Excel PowerPoint'),
]
FIELDS = ('text', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_answer')


def update_questions(apps, schema_editor):
    from olympiad.tests_data import TESTS

    Question = apps.get_model('olympiad', 'Question')
    data = {(subject, level): items for subject, levels in TESTS for level, _minutes, items in levels}
    for subject, level in LEVELS:
        items = data.get((subject, level)) or []
        questions = list(Question.objects.filter(level__subject__name=subject, level__name=level).order_by('id'))
        # Faqat savollar soni mos kelsa yangilanadi; bo'sh daraja seed_demo orqali yangidan to'ladi.
        if len(questions) != len(items):
            continue
        for question, item in zip(questions, items):
            for field in FIELDS:
                setattr(question, field, item[field])
            question.save(update_fields=list(FIELDS))


class Migration(migrations.Migration):
    dependencies = [('olympiad', '0025_antalya_tests')]
    operations = [migrations.RunPython(update_questions, migrations.RunPython.noop)]

from django.db import migrations

# Foydalanuvchi so'rovi (2026-10-22): Starter.png dagi test Starter darajasiga,
# Beginner.png dagi test Beginner darajasiga qo'yiladi. Avval ular teskari yuklangan edi.
# Savollar o'chirilmaydi, faqat darajasi almashtiriladi: allaqachon ishlangan
# natijalardagi javoblar saqlanib qoladi.
KIDS_TEST_FIRST_QUESTION = 'is pointing at the girl'


def swap(apps, schema_editor):
    Subject = apps.get_model('olympiad', 'Subject')
    Level = apps.get_model('olympiad', 'Level')
    Question = apps.get_model('olympiad', 'Question')

    subject = Subject.objects.filter(name='English').first()
    if not subject:
        return
    starter = Level.objects.filter(subject=subject, name='Starter').first()
    beginner = Level.objects.filter(subject=subject, name='Beginner').first()
    if not starter or not beginner:
        return
    # Faqat eski (teskari) holatda bo'lsa almashtiriladi.
    if not Question.objects.filter(level=starter, text__contains=KIDS_TEST_FIRST_QUESTION).exists():
        return

    starter_ids = list(Question.objects.filter(level=starter).values_list('id', flat=True))
    Question.objects.filter(level=beginner).update(level=starter)
    Question.objects.filter(id__in=starter_ids).update(level=beginner)


class Migration(migrations.Migration):

    dependencies = [
        ('olympiad', '0021_remove_old_empty_levels'),
    ]

    operations = [
        migrations.RunPython(swap, migrations.RunPython.noop),
    ]

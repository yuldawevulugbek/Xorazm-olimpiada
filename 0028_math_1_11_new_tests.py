# 2026-10-24: Matematika 1–11-sinf testlari foydalanuvchining yangi "Matem" arxividagi testlar bilan almashtirildi.
# Shu darajalarning eski savollari o'chiriladi, start_railway.sh dagi seed_demo yangilarini tests_data.py dan yuklaydi.
# O'quvchilar, darajalar va natijalar (ball) saqlanib qoladi.
from django.db import migrations

GRADES = [f'{n}-sinf' for n in range(1, 12)]


def clear_math_1_11(apps, schema_editor):
    Question = apps.get_model('olympiad', 'Question')
    Question.objects.filter(level__subject__name='Matematika', level__name__in=GRADES).delete()


class Migration(migrations.Migration):
    dependencies = [('olympiad', '0027_all_levels_30_minutes')]
    operations = [migrations.RunPython(clear_math_1_11, migrations.RunPython.noop)]

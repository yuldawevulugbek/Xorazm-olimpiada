# 2026-10-24: barcha testlar vaqti 30 daqiqa (eski darajalarda 60 qolgan bo'lishi mumkin edi).
from django.db import migrations


def set_30_minutes(apps, schema_editor):
    Level = apps.get_model('olympiad', 'Level')
    Level.objects.exclude(duration_minutes=30).update(duration_minutes=30)


class Migration(migrations.Migration):
    dependencies = [('olympiad', '0026_rebalance_answer_keys')]
    operations = [migrations.RunPython(set_30_minutes, migrations.RunPython.noop)]

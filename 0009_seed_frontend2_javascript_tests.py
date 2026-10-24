from django.db import migrations


def noop(apps, schema_editor):
    # Test/daraja seedlari olib tashlandi. Faqat Mental arifmetika qoldiriladi.
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('olympiad', '0008_seed_rus_tili_harder_tests'),
    ]

    operations = [
        migrations.RunPython(noop, migrations.RunPython.noop),
    ]

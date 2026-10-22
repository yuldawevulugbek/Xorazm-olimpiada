from django.db import migrations


def noop(apps, schema_editor):
    # Test/daraja seedlari olib tashlandi. Faqat Mental arifmetika qoldiriladi.
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('olympiad', '0009_seed_frontend2_javascript_tests'),
    ]

    operations = [
        migrations.RunPython(noop, migrations.RunPython.noop),
    ]

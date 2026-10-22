from django.db import migrations


def clear_existing_branches(apps, schema_editor):
    Branch = apps.get_model('olympiad', 'Branch')
    Branch.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('olympiad', '0012_remix_backend_math5_options'),
    ]

    operations = [
        migrations.RunPython(clear_existing_branches, migrations.RunPython.noop),
    ]

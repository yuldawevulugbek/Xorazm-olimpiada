# Generated for dynamic branch management
from django.db import migrations, models


DEFAULT_BRANCHES = []


def seed_default_branches(apps, schema_editor):
    Branch = apps.get_model('olympiad', 'Branch')
    for name in DEFAULT_BRANCHES:
        Branch.objects.get_or_create(name=name)


class Migration(migrations.Migration):

    dependencies = [
        ('olympiad', '0003_student_branch'),
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.AlterField(
            model_name='student',
            name='branch',
            field=models.CharField(default='Boshqa', max_length=100),
        ),
        migrations.RunPython(seed_default_branches, migrations.RunPython.noop),
    ]

# Generated for student exam resume progress.
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('olympiad', '0004_branch_dynamic'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='progress_answers',
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AddField(
            model_name='student',
            name='progress_remaining_seconds',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='progress_current_index',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='student',
            name='progress_updated_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]

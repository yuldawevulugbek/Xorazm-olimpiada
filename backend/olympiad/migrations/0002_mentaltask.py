# Generated for mental arithmetic mode
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('olympiad', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MentalTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_order', models.PositiveIntegerField()),
                ('flashes', models.JSONField(default=list)),
                ('expression', models.CharField(max_length=255)),
                ('correct_answer', models.IntegerField()),
                ('student_answer', models.IntegerField(blank=True, null=True)),
                ('is_correct', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('result', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='mental_answers', to='olympiad.result')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mental_tasks', to='olympiad.student')),
            ],
            options={
                'ordering': ['task_order'],
                'unique_together': {('student', 'task_order')},
            },
        ),
    ]

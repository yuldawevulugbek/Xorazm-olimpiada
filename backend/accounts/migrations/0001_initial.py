# Generated for branch based admin profiles
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('olympiad', '0002_mentaltask'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('branch', models.CharField(choices=[('Niyozbosh', 'Niyozbosh'), ('Xalqabod', 'Xalqabod'), ('Gulbahor', 'Gulbahor'), ('Kasblar', 'Kasblar'), ('Kids1', 'Kids1'), ('Kids2', 'Kids2'), ('Do’stobod', 'Do’stobod'), ('Olmazor', 'Olmazor'), ('Chinoz', 'Chinoz'), ('Krasin', 'Krasin'), ('Pitiletka', 'Pitiletka'), ('Qo’rg’oncha', 'Qo’rg’oncha'), ('Kids 3', 'Kids 3'), ('Oqqo’rg’on', 'Oqqo’rg’on'), ('Alimkent', 'Alimkent'), ('Boshqa', 'Boshqa')], max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='admin_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['branch', 'user__username'],
            },
        ),
    ]

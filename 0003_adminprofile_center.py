# Generated for center based admin profiles
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('olympiad', '0004_branch_dynamic'),
        ('accounts', '0002_alter_adminprofile_branch'),
    ]

    operations = [
        migrations.AddField(
            model_name='adminprofile',
            name='center',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='admin_profiles', to='olympiad.center'),
        ),
        migrations.AlterField(
            model_name='adminprofile',
            name='branch',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]

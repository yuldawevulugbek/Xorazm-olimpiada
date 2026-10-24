# Generated for dynamic branch management
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adminprofile',
            name='branch',
            field=models.CharField(max_length=100),
        ),
    ]

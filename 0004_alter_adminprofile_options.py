# Generated to match AdminProfile model options
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_adminprofile_center'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='adminprofile',
            options={'ordering': ['center__name', 'branch', 'user__username']},
        ),
    ]

# Generated for branch based student filtering
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('olympiad', '0002_mentaltask'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='branch',
            field=models.CharField(choices=[('Niyozbosh', 'Niyozbosh'), ('Xalqabod', 'Xalqabod'), ('Gulbahor', 'Gulbahor'), ('Kasblar', 'Kasblar'), ('Kids1', 'Kids1'), ('Kids2', 'Kids2'), ('Do’stobod', 'Do’stobod'), ('Olmazor', 'Olmazor'), ('Chinoz', 'Chinoz'), ('Krasin', 'Krasin'), ('Pitiletka', 'Pitiletka'), ('Qo’rg’oncha', 'Qo’rg’oncha'), ('Kids 3', 'Kids 3'), ('Oqqo’rg’on', 'Oqqo’rg’on'), ('Alimkent', 'Alimkent'), ('Boshqa', 'Boshqa')], default='Boshqa', max_length=50),
        ),
    ]

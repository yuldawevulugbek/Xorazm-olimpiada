from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('olympiad', '0019_clear_all_tests'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='image_url',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='question',
            name='option_c',
            field=models.CharField(blank=True, default='', max_length=500),
        ),
        migrations.AlterField(
            model_name='question',
            name='option_d',
            field=models.CharField(blank=True, default='', max_length=500),
        ),
    ]

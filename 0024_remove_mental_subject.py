from django.db import migrations


def remove_mental_subject(apps, schema_editor):
    """Mental arifmetika fani loyihadan olib tashlandi: fan, darajalari, o'quvchilari va natijalari o'chiriladi."""
    Subject = apps.get_model('olympiad', 'Subject')
    Student = apps.get_model('olympiad', 'Student')

    mental_subjects = [subject for subject in Subject.objects.all() if 'mental' in subject.name.lower()]
    for subject in mental_subjects:
        Student.objects.filter(subject=subject).delete()
        subject.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('olympiad', '0023_student_age_self_registered'),
    ]

    operations = [
        migrations.RunPython(remove_mental_subject, migrations.RunPython.noop),
    ]

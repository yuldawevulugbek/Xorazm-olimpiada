import os

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from olympiad.models import Center, Subject, Level
from olympiad.tests_loader import load_tests, merge_duplicate_subjects, move_students_to_test_levels


class Command(BaseCommand):
    help = 'Demo admin, markaz va faqat Mental arifmetika fanini yaratadi.'

    def handle(self, *args, **options):
        User.objects.filter(username='admin').delete()
        admin_user, _ = User.objects.get_or_create(
            username='ulugbek',
            defaults={
                'email': 'ulugbek@example.com',
                'is_staff': True,
                'is_superuser': True,
                'is_active': True,
            }
        )
        admin_user.email = admin_user.email or 'ulugbek@example.com'
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.is_active = True
        # Parolni Railway Variables'dagi ADMIN_PASSWORD orqali o'zgartirish mumkin.
        # Yozilmagan bo'lsa, avvalgi parol ishlaydi.
        admin_password = os.getenv('ADMIN_PASSWORD') or 'codingwithulugbek20030313'
        admin_user.set_password(admin_password)
        admin_user.save()

        Center.objects.get_or_create(name='Al-Aziz Academy')

        mental_subject, _ = Subject.objects.get_or_create(name='Mental arifmetika')
        mental_level, _ = Level.objects.get_or_create(
            subject=mental_subject,
            name='Mental A',
            defaults={'duration_minutes': 5},
        )
        mental_level.duration_minutes = 5
        mental_level.save(update_fields=['duration_minutes'])

        merged = merge_duplicate_subjects()
        added = load_tests()
        moved = move_students_to_test_levels()

        self.stdout.write(self.style.SUCCESS('Admin login tayyor: ulugbek (parol ADMIN_PASSWORD yoki standart)'))
        self.stdout.write(self.style.SUCCESS(f'Mental arifmetika, Matematika (1–11-sinf), English, Rus tili, IT Frontend va IT Backend testlari tayyor. Yangi qo‘shilgan savollar: {added}. Testli darajaga o‘tkazilgan o‘quvchilar: {moved}. Birlashtirilgan takroriy fanlar: {merged}.'))

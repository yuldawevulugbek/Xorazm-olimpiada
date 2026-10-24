from .models import Subject, Level, Question, Student
from .tests_data import TESTS

# Excel'da yoziladigan fan nomlari -> bazadagi testli fan nomi
SUBJECT_ALIASES = {
    'ingliz tili': 'English',
    'ingliz': 'English',
    'english': 'English',
    'matem': 'Matematika',
    'matematika': 'Matematika',
    'math': 'Matematika',
    'rus tili': 'Rus tili',
    'rus': 'Rus tili',
    'frontend': 'IT Frontend',
    'it frontend': 'IT Frontend',
    'backend': 'IT Backend',
    'it backend': 'IT Backend',
    'mental': 'Mental arifmetika',
    'mental arifmetika': 'Mental arifmetika',
    'arab': 'Arab tili',
    'arab tili': 'Arab tili',
    'koreys': 'Koreys tili',
    'koreys tili': 'Koreys tili',
}


def canonical_subject_name(name):
    return SUBJECT_ALIASES.get(name_key(name), str(name or '').strip())


def name_key(text):
    return ' '.join(str(text or '').replace('‘', "'").replace('’', "'").lower().split())


def normalize_level_key(level_name):
    key = name_key(level_name)
    if key.isdigit():
        key = f'{key}-sinf'
    return key.replace(' sinf', '-sinf')


def load_tests():
    """tests_data.py dagi testlarni bazaga yozadi.

    Savollari bor darajaga tegilmaydi: admin paneldagi o'zgarishlar va o'quvchilarning
    javoblari har deploy'da o'chib ketmasligi uchun faqat bo'sh darajalar to'ldiriladi.
    """
    added = 0
    for subject_name, levels in TESTS:
        subject, _ = Subject.objects.get_or_create(name=subject_name)
        for level_name, duration_minutes, questions in levels:
            level, created = Level.objects.get_or_create(
                subject=subject,
                name=level_name,
                defaults={'duration_minutes': duration_minutes},
            )
            if Question.objects.filter(subject=subject, level=level).exists():
                continue
            if not created:
                level.duration_minutes = duration_minutes
                level.save(update_fields=['duration_minutes'])
            Question.objects.bulk_create([
                Question(subject=subject, level=level, version=1, **item)
                for item in questions
            ])
            added += len(questions)
    return added


def move_students_to_test_levels():
    """Testni hali boshlamagan, savolsiz darajadagi o'quvchilarni mos testli darajaga o'tkazadi.

    Masalan: "INGLIZ TILI / STARTER" -> "English / Starter", "MATEM / 3-SINF" -> "Matematika / 3-sinf".
    """
    levels_with_tests = {}
    for level in Level.objects.select_related('subject').filter(questions__isnull=False).distinct():
        levels_with_tests[(name_key(level.subject.name), name_key(level.name))] = level

    moved = 0
    students = Student.objects.select_related('subject', 'level').filter(status=Student.Status.NOT_STARTED)
    for student in students:
        if Question.objects.filter(level=student.level).exists():
            continue
        subject_key = name_key(SUBJECT_ALIASES.get(name_key(student.subject.name), student.subject.name))
        target = levels_with_tests.get((subject_key, normalize_level_key(student.level.name)))
        if target:
            student.subject = target.subject
            student.level = target
            student.save(update_fields=['subject', 'level'])
            moved += 1
    return moved


def _merge_level_into(source, target):
    """source darajadagi o'quvchi va savollarni target darajaga o'tkazib, source ni o'chiradi."""
    Student.objects.filter(level=source).update(subject=target.subject, level=target)
    Question.objects.filter(level=source).update(subject=target.subject, level=target)
    source.delete()


def merge_duplicate_subjects():
    """Bir xil fanning ikki xil yozilishini bittaga birlashtiradi.

    Masalan: "INGLIZ TILI" -> "English", "MATEM" -> "Matematika", "MENTAL" / "Mental" ->
    "Mental arifmetika", "RUS TILI" -> "Rus tili". O'quvchilar, natijalar va savollar
    saqlanib qoladi, faqat to'g'ri fan va darajaga o'tkaziladi. Bir xil darajalar
    ("3-SINF" va "3-sinf") ham bittaga birlashtiriladi.
    """
    groups = {}
    for subject in Subject.objects.all().order_by('id'):
        groups.setdefault(name_key(canonical_subject_name(subject.name)), []).append(subject)

    merged = 0
    for subjects in groups.values():
        canonical = canonical_subject_name(subjects[0].name)
        # Asosiy fan: nomi to'g'ri yozilgani, bo'lmasa savollari eng ko'p bo'lgani.
        target = next((item for item in subjects if item.name == canonical), None)
        if target is None:
            target = max(subjects, key=lambda item: (item.questions.count(), -item.id))
            target.name = canonical
            target.save(update_fields=['name'])

        for subject in subjects:
            if subject.id == target.id:
                continue
            for level in list(subject.levels.all()):
                key = normalize_level_key(level.name)
                same = next((item for item in target.levels.all() if normalize_level_key(item.name) == key), None)
                if same:
                    _merge_level_into(level, same)
                else:
                    level.subject = target
                    level.save(update_fields=['subject'])
                    Student.objects.filter(level=level).update(subject=target)
                    Question.objects.filter(level=level).update(subject=target)
            Student.objects.filter(subject=subject).update(subject=target)
            subject.delete()
            merged += 1

        # Bitta fan ichida bir xil daraja ikki marta yozilgan bo'lsa ("3-SINF" va "3-sinf").
        by_key = {}
        for level in target.levels.all().order_by('id'):
            by_key.setdefault(normalize_level_key(level.name), []).append(level)
        for levels in by_key.values():
            if len(levels) < 2:
                continue
            keep = max(levels, key=lambda item: (item.questions.count(), -item.id))
            for level in levels:
                if level.id != keep.id:
                    _merge_level_into(level, keep)
    return merged

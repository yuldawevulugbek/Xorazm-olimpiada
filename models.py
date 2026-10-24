import random
from django.db import models
from django.utils import timezone


# Filiallar endi oldindan qattiq ro'yxat qilib berilmaydi.
# Admin Excel yuklaganda yoki paneldan qo'shganda filial avtomatik Branch jadvaliga yoziladi.
DEFAULT_BRANCHES = []

BRANCH_CHOICES = tuple((branch, branch) for branch in DEFAULT_BRANCHES)


class Center(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Branch(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Level(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='levels')
    name = models.CharField(max_length=255)
    duration_minutes = models.PositiveIntegerField(default=30)

    class Meta:
        unique_together = ('subject', 'name')
        ordering = ['subject__name', 'name']

    def __str__(self):
        return f'{self.subject.name} - {self.name}'


class Student(models.Model):
    class Status(models.TextChoices):
        NOT_STARTED = 'not_started', 'Ishlamagan'
        IN_PROGRESS = 'in_progress', 'Ishlayapti'
        COMPLETED = 'completed', 'Ishlab bo‘ldi'

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT, related_name='students')
    level = models.ForeignKey(Level, on_delete=models.PROTECT, related_name='students')
    selected_version = models.PositiveSmallIntegerField(null=True, blank=True)
    center = models.ForeignKey(Center, on_delete=models.PROTECT, related_name='students')
    branch = models.CharField(max_length=100, default='Boshqa')
    age = models.PositiveSmallIntegerField(null=True, blank=True)
    # O'quvchi o'zi "Ro'yxatdan o'tish" orqali kirgan bo'lsa True (admin yaratgan bo'lsa False).
    is_self_registered = models.BooleanField(default=False)
    code = models.CharField(max_length=6, unique=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NOT_STARTED)
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    is_used = models.BooleanField(default=False)
    progress_answers = models.JSONField(default=dict, blank=True)
    progress_remaining_seconds = models.PositiveIntegerField(null=True, blank=True)
    progress_current_index = models.PositiveIntegerField(default=0)
    progress_updated_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'.strip()

    def __str__(self):
        return f'{self.full_name} - {self.code}'

    @staticmethod
    def generate_code():
        while True:
            code = str(random.randint(100000, 999999))
            if not Student.objects.filter(code=code).exists():
                return code

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_code()
        super().save(*args, **kwargs)


class Question(models.Model):
    ANSWER_CHOICES = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
    )

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='questions')
    level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name='questions')
    version = models.PositiveSmallIntegerField(default=1)
    text = models.TextField()
    option_a = models.CharField(max_length=500)
    option_b = models.CharField(max_length=500)
    option_c = models.CharField(max_length=500, blank=True, default='')
    option_d = models.CharField(max_length=500, blank=True, default='')
    image_url = models.CharField(max_length=255, blank=True, default='')
    correct_answer = models.CharField(max_length=1, choices=ANSWER_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'{self.subject.name} / {self.level.name} / Version {self.version} / {self.text[:40]}'


class Result(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='result')
    total_questions = models.PositiveIntegerField(default=0)
    correct_count = models.PositiveIntegerField(default=0)
    percent = models.FloatField(default=0)
    started_at = models.DateTimeField(default=timezone.now)
    finished_at = models.DateTimeField(default=timezone.now)
    spent_seconds = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.student.full_name} - {self.correct_count}/{self.total_questions}'


class StudentAnswer(models.Model):
    result = models.ForeignKey(Result, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_answer = models.CharField(max_length=1, blank=True)
    is_correct = models.BooleanField(default=False)

    class Meta:
        unique_together = ('result', 'question')


class MentalTask(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='mental_tasks')
    result = models.ForeignKey(Result, on_delete=models.SET_NULL, null=True, blank=True, related_name='mental_answers')
    task_order = models.PositiveIntegerField()
    flashes = models.JSONField(default=list)
    expression = models.CharField(max_length=255)
    correct_answer = models.IntegerField()
    student_answer = models.IntegerField(null=True, blank=True)
    is_correct = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['task_order']
        unique_together = ('student', 'task_order')

    def __str__(self):
        return f'{self.student.full_name} / mental #{self.task_order}'

from django.contrib import admin
from .models import Center, Branch, Subject, Level, Student, Question, Result, StudentAnswer, MentalTask


@admin.register(Center)
class CenterAdmin(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'duration_minutes']
    list_filter = ['subject']
    search_fields = ['name', 'subject__name']


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'subject', 'level', 'selected_version', 'center', 'branch', 'code', 'status', 'is_used', 'created_at']
    list_filter = ['status', 'subject', 'level', 'selected_version', 'center', 'branch']
    search_fields = ['first_name', 'last_name', 'code']
    readonly_fields = ['code', 'created_at']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'subject', 'level', 'version', 'correct_answer']
    list_filter = ['subject', 'level', 'version']
    search_fields = ['text']


class StudentAnswerInline(admin.TabularInline):
    model = StudentAnswer
    extra = 0


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ['student', 'correct_count', 'total_questions', 'percent', 'spent_seconds', 'created_at']
    search_fields = ['student__first_name', 'student__last_name', 'student__code']
    inlines = [StudentAnswerInline]


@admin.register(MentalTask)
class MentalTaskAdmin(admin.ModelAdmin):
    list_display = ('student', 'task_order', 'expression', 'correct_answer', 'student_answer', 'is_correct')
    list_filter = ('is_correct', 'student__subject')
    search_fields = ('student__first_name', 'student__last_name', 'student__code', 'expression')

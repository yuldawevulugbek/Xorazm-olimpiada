from rest_framework import serializers
from .models import Center, Branch, Subject, Level, Student, Question, Result, StudentAnswer, MentalTask


class CenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Center
        fields = ['id', 'name']

    def validate_name(self, value):
        clean = str(value or '').strip()
        if not clean:
            raise serializers.ValidationError('O‘quv markaz nomini kiriting.')
        return clean


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ['id', 'name', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_name(self, value):
        clean = str(value or '').strip()
        if not clean:
            raise serializers.ValidationError('Filial nomini kiriting.')
        return clean


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name']

    def validate_name(self, value):
        # "Matematika" bor bo'lsa "MATEM" yoki "matematika" degan ikkinchi fan ochilmasin.
        from .tests_loader import canonical_subject_name, name_key

        key = name_key(canonical_subject_name(value))
        for subject in Subject.objects.exclude(pk=getattr(self.instance, 'pk', None)):
            if name_key(canonical_subject_name(subject.name)) == key:
                raise serializers.ValidationError(f'"{subject.name}" fani allaqachon bor.')
        return value.strip()


class LevelSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source='subject.name', read_only=True)

    class Meta:
        model = Level
        fields = ['id', 'subject', 'subject_name', 'name', 'duration_minutes']


class StudentSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    level_name = serializers.CharField(source='level.name', read_only=True)
    center_name = serializers.CharField(source='center.name', read_only=True)
    branch_display = serializers.SerializerMethodField()
    full_name = serializers.CharField(read_only=True)
    correct_count = serializers.SerializerMethodField()
    total_questions = serializers.SerializerMethodField()
    percent = serializers.SerializerMethodField()
    spent_seconds = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = [
            'id', 'first_name', 'last_name', 'full_name', 'subject', 'subject_name',
            'level', 'level_name', 'selected_version', 'center', 'center_name', 'branch', 'branch_display', 'age', 'is_self_registered', 'code', 'status',
            'started_at', 'finished_at', 'is_used', 'progress_remaining_seconds', 'progress_current_index',
            'progress_updated_at', 'created_at', 'correct_count', 'total_questions', 'percent', 'spent_seconds'
        ]
        read_only_fields = [
            'is_self_registered', 'code', 'status', 'started_at', 'finished_at', 'is_used', 'selected_version', 'progress_remaining_seconds',
            'progress_current_index', 'progress_updated_at', 'created_at'
        ]

    def get_branch_display(self, obj):
        return obj.branch

    def get_correct_count(self, obj):
        return getattr(getattr(obj, 'result', None), 'correct_count', None)

    def get_total_questions(self, obj):
        return getattr(getattr(obj, 'result', None), 'total_questions', None)

    def get_percent(self, obj):
        return getattr(getattr(obj, 'result', None), 'percent', None)

    def get_spent_seconds(self, obj):
        return getattr(getattr(obj, 'result', None), 'spent_seconds', None)

    def validate(self, attrs):
        subject = attrs.get('subject') or getattr(self.instance, 'subject', None)
        level = attrs.get('level') or getattr(self.instance, 'level', None)
        if subject and level and level.subject_id != subject.id:
            raise serializers.ValidationError({'level': 'Tanlangan daraja shu fanga tegishli emas.'})
        return attrs


class QuestionAdminSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    level_name = serializers.CharField(source='level.name', read_only=True)

    class Meta:
        model = Question
        fields = [
            'id', 'subject', 'subject_name', 'level', 'level_name', 'version', 'text',
            'option_a', 'option_b', 'option_c', 'option_d', 'image_url', 'correct_answer', 'created_at'
        ]


class QuestionForExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'version', 'text', 'option_a', 'option_b', 'option_c', 'option_d', 'image_url']


class StudentAnswerSerializer(serializers.ModelSerializer):
    question_text = serializers.CharField(source='question.text', read_only=True)
    option_a = serializers.CharField(source='question.option_a', read_only=True)
    option_b = serializers.CharField(source='question.option_b', read_only=True)
    option_c = serializers.CharField(source='question.option_c', read_only=True)
    option_d = serializers.CharField(source='question.option_d', read_only=True)
    correct_answer = serializers.CharField(source='question.correct_answer', read_only=True)

    class Meta:
        model = StudentAnswer
        fields = [
            'id', 'question', 'question_text',
            'option_a', 'option_b', 'option_c', 'option_d',
            'selected_answer', 'correct_answer', 'is_correct'
        ]


class MentalTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = MentalTask
        fields = ['id', 'task_order', 'expression', 'correct_answer', 'student_answer', 'is_correct']


class ResultSerializer(serializers.ModelSerializer):
    student_full_name = serializers.CharField(source='student.full_name', read_only=True)
    student_code = serializers.CharField(source='student.code', read_only=True)
    subject_name = serializers.CharField(source='student.subject.name', read_only=True)
    level_name = serializers.CharField(source='student.level.name', read_only=True)
    center_name = serializers.CharField(source='student.center.name', read_only=True)
    student_branch = serializers.CharField(source='student.branch', read_only=True)
    student_selected_version = serializers.IntegerField(source='student.selected_version', read_only=True)
    answers = StudentAnswerSerializer(many=True, read_only=True)
    mental_answers = MentalTaskSerializer(many=True, read_only=True)

    class Meta:
        model = Result
        fields = [
            'id', 'student', 'student_full_name', 'student_code', 'subject_name',
            'level_name', 'student_selected_version', 'center_name', 'student_branch', 'total_questions', 'correct_count',
            'percent', 'started_at', 'finished_at', 'spent_seconds', 'created_at', 'answers', 'mental_answers'
        ]

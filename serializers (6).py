from django.contrib.auth.models import User
from rest_framework import serializers

from olympiad.models import Branch, Center
from .models import AdminProfile


class AdminUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6, required=False)
    branch = serializers.CharField(required=False, allow_blank=True)
    center = serializers.IntegerField(required=False, allow_null=True, write_only=True)
    center_name = serializers.CharField(source='admin_profile.center.name', read_only=True)
    is_main_admin = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'first_name', 'last_name', 'email', 'password',
            'is_staff', 'is_superuser', 'is_main_admin', 'center', 'center_name',
            'branch', 'date_joined'
        ]
        read_only_fields = ['id', 'is_staff', 'is_superuser', 'is_main_admin', 'center_name', 'date_joined']

    def get_is_main_admin(self, obj):
        profile = getattr(obj, 'admin_profile', None)
        return bool(obj.is_superuser or not profile or (not profile.center_id and not profile.branch))

    def to_representation(self, instance):
        data = super().to_representation(instance)
        profile = getattr(instance, 'admin_profile', None)
        data['branch'] = getattr(profile, 'branch', '') if profile else ''
        data['center'] = getattr(profile, 'center_id', None) if profile else None
        data['center_name'] = getattr(getattr(profile, 'center', None), 'name', '') if profile else ''
        return data

    def validate(self, attrs):
        request = self.context.get('request')
        if request and request.method == 'POST' and not attrs.get('password'):
            raise serializers.ValidationError({'password': 'Parol kiritish majburiy.'})

        branch = str(attrs.get('branch') or '').strip()
        if branch and not Branch.objects.filter(name__iexact=branch).exists():
            raise serializers.ValidationError({'branch': 'Bunday filial topilmadi. Avval filialni qo‘shing.'})
        if branch:
            attrs['branch'] = Branch.objects.filter(name__iexact=branch).first().name

        center_id = attrs.get('center')
        if request and request.method == 'POST' and not center_id:
            raise serializers.ValidationError({'center': 'Admin uchun o‘quv markaz tanlash majburiy.'})
        if center_id:
            try:
                attrs['center'] = Center.objects.get(id=center_id)
            except Center.DoesNotExist:
                raise serializers.ValidationError({'center': 'Bunday o‘quv markaz topilmadi.'})
        return attrs

    def create(self, validated_data):
        request = self.context.get('request')
        password = validated_data.pop('password')
        branch = validated_data.pop('branch', '')
        center = validated_data.pop('center', None)

        creator = getattr(request, 'user', None)
        creator_profile = getattr(creator, 'admin_profile', None) if creator and creator.is_authenticated else None
        if creator_profile and creator_profile.center_id:
            center = creator_profile.center
            branch = creator_profile.branch

        if not center:
            raise serializers.ValidationError({'center': 'Admin uchun o‘quv markaz tanlash majburiy.'})

        user = User(**validated_data)
        user.is_staff = True
        user.is_superuser = False
        user.set_password(password)
        user.save()
        AdminProfile.objects.create(user=user, center=center, branch=branch)
        return user

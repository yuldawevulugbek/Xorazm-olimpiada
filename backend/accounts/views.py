from django.contrib.auth.models import User
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import AdminUserSerializer


def get_admin_branch(user):
    return getattr(getattr(user, 'admin_profile', None), 'branch', '')


def get_admin_center(user):
    profile = getattr(user, 'admin_profile', None)
    return getattr(profile, 'center', None)


def is_main_admin(user):
    profile = getattr(user, 'admin_profile', None) if user and user.is_authenticated else None
    return bool(user and user.is_authenticated and user.is_staff and (user.is_superuser or not profile or (not profile.center_id and not profile.branch)))


class IsStaffAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)


class CanManageAdmins(permissions.BasePermission):
    def has_permission(self, request, view):
        # Faqat bosh admin yangi o‘quv markaz adminlarini yaratadi.
        return is_main_admin(request.user)


class AdminUserListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = AdminUserSerializer
    permission_classes = [CanManageAdmins]

    def get_queryset(self):
        return User.objects.filter(is_staff=True).select_related('admin_profile', 'admin_profile__center').order_by('-date_joined')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class CurrentAdminAPIView(APIView):
    permission_classes = [IsStaffAdmin]

    def get(self, request):
        serializer = AdminUserSerializer(request.user, context={'request': request})
        data = serializer.data
        main_admin = is_main_admin(request.user)
        center = get_admin_center(request.user)
        data['can_manage_admins'] = main_admin
        data['can_manage_centers'] = main_admin
        data['can_create_students'] = bool(main_admin or center)
        data['can_edit_students'] = bool(main_admin or center)
        data['can_delete_students'] = bool(main_admin or center)
        data['assigned_center'] = center.id if center else None
        data['assigned_center_name'] = center.name if center else ''
        return Response(data)

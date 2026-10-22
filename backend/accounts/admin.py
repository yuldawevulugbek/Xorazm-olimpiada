from django.contrib import admin

from .models import AdminProfile


@admin.register(AdminProfile)
class AdminProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'center', 'branch', 'created_at']
    list_filter = ['center', 'branch']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'center__name', 'branch']

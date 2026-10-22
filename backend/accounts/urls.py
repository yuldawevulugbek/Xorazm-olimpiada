from django.urls import path
from .views import AdminUserListCreateAPIView, CurrentAdminAPIView

urlpatterns = [
    path('admins/', AdminUserListCreateAPIView.as_view(), name='admins'),
    path('me/', CurrentAdminAPIView.as_view(), name='current-admin'),
]

from django.conf import settings
from django.db import models


class AdminProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='admin_profile')
    center = models.ForeignKey(
        'olympiad.Center',
        on_delete=models.SET_NULL,
        related_name='admin_profiles',
        null=True,
        blank=True,
    )
    branch = models.CharField(max_length=100, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['center__name', 'branch', 'user__username']

    def __str__(self):
        center_name = self.center.name if self.center else 'Bosh admin'
        return f'{self.user.username} - {center_name}'

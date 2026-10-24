from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Question


@receiver(post_save, sender=Question)
@receiver(post_delete, sender=Question)
def clear_exam_questions_cache(sender, instance, **kwargs):
    # Admin savolni o'zgartirsa, keshdagi eski savollar darhol tashlanadi.
    from .views import exam_questions_cache_key

    cache.delete(exam_questions_cache_key(instance.subject_id, instance.level_id, instance.version or 1))
    # Ro'yxatdan o'tish oynasidagi fan/daraja ro'yxati ham yangilansin.
    cache.delete('registration-catalog')

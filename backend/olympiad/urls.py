from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CenterViewSet,
    BranchViewSet,
    SubjectViewSet,
    LevelViewSet,
    StudentViewSet,
    QuestionViewSet,
    ResultViewSet,
    ExamStartAPIView,
    ExamProgressSaveAPIView,
    ExamSubmitAPIView,
    PublicResultLookupAPIView,
    ExamCatalogAPIView,
    ExamRegisterAPIView,
)

router = DefaultRouter()
router.register('centers', CenterViewSet, basename='centers')
router.register('branches', BranchViewSet, basename='branches')
router.register('subjects', SubjectViewSet, basename='subjects')
router.register('levels', LevelViewSet, basename='levels')
router.register('students', StudentViewSet, basename='students')
router.register('questions', QuestionViewSet, basename='questions')
router.register('results', ResultViewSet, basename='results')

urlpatterns = [
    path('', include(router.urls)),
    path('exam/catalog/', ExamCatalogAPIView.as_view(), name='exam-catalog'),
    path('exam/register/', ExamRegisterAPIView.as_view(), name='exam-register'),
    path('exam/start/', ExamStartAPIView.as_view(), name='exam-start'),
    path('exam/progress/', ExamProgressSaveAPIView.as_view(), name='exam-progress'),
    path('exam/submit/', ExamSubmitAPIView.as_view(), name='exam-submit'),
    path('exam/result/', PublicResultLookupAPIView.as_view(), name='exam-result'),
]

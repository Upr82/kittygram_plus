from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import AchievementViewSet, CatViewSet, OwnerViewSet

app_name = 'cats'

router = DefaultRouter()
router.register('cats', CatViewSet)
router.register('owners', OwnerViewSet)
router.register('achievements', AchievementViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
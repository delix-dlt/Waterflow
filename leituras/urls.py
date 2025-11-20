from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LeituraViewSet

router = DefaultRouter()
router.register('leituras', LeituraViewSet, basename='leituras')

urlpatterns = [
    path('', include(router.urls)),
]

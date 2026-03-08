from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LeituraViewSet
from .views_dashboard import dashboard  # Importar a view da dashboard

router = DefaultRouter()
router.register('leituras', LeituraViewSet, basename='leituras')

urlpatterns = [
    path('', include(router.urls)),
    path('dashboard/', dashboard, name='dashboard'),  # Esta linha é essencial
]

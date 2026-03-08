# sistema_agua/urls.py
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from django.conf.urls.static import static

# Só importa a dashboard (já não precisas do home_redirect)
from leituras.views_dashboard import dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('leituras.urls')),

    # Login bonito para todos os usuários
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='/login/'), name='logout'),

    # Dashboard do cliente
    path('dashboard/', dashboard, name='dashboard'),

    # Raiz vai direto para login ou dashboard (segundo o usuário)
    path('', dashboard, name='home'),  # quem estiver logado vai para dashboard, quem não estiver vai para login
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
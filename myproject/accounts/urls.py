from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import (
    register,
    projeto_detalhes,
    login_view,
    home,
    projetos,
    perfil,
    edit_profile,
    portfolio,
    add_portfolio,
    edit_skills,
    send_message,
    adicionar_projeto
)

urlpatterns = [
    path('', login_view, name='login'),
    path('login/', login_view, name='login'),
    path('register/', register, name='register'),
    path('home/', home, name='home'),
    path('projetos/', projetos, name='projetos'),
    path('perfil/', perfil, name='perfil'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('portfolio/', portfolio, name='portfolio'),
    path('add_portfolio/', add_portfolio, name='add_portfolio'),
    path('edit_skills/', edit_skills, name='edit_skills'),
    path('send_message/', send_message, name='send_message'),
    path('adicionar_projeto/', adicionar_projeto, name='adicionar_projeto'),
    path('projeto/<int:id>/', projeto_detalhes, name='projeto_detalhes'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

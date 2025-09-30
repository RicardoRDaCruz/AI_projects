from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("api/process-prompt/", views.process_prompt, name='process-prompt'),
    path("mapa_info/", views.mapa_prompt, name='mapa-prompt')
]
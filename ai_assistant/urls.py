from django.urls import path
from . import views

app_name = 'ai_assistant'

urlpatterns = [
    path('chat/', views.chat, name='chat'),
    path('transcribe/', views.transcribe, name='transcribe'),
    path('health/', views.health_check, name='health'),
]

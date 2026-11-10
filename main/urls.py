from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('resume/', views.resume_view, name='resume'),
    path('uploading-soon/', views.uploading_soon, name='uploading_soon'),
    path('live-demo-soon/', views.live_demo_soon, name='live_demo_soon'),
    path('github-soon/', views.github_soon, name='github_soon'),
    path('revamp/', views.revamp_preview, name='revamp_preview'),
    path('game/', views.game_world, name='game_world'),
]
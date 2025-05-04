from django.urls import path
from . import views

urlpatterns = [
    path('', views.assistant_home, name='assistant'),
    path('chat/<int:session_id>/', views.assistant_chat, name='assistant_chat'),
] 
from django.urls import path
from . import views

urlpatterns = [
    path('', views.skill_list, name='skill_list'),
    path('add/', views.add_skill, name='add_skill'),
    path('delete/<int:skill_id>/', views.delete_skill, name='delete_skill'),
    path('matches/', views.matches, name='matches'),
    path('assistant/', views.ai_assistant, name='ai_assistant'),
    path('chat-history/<int:user_id>/', views.chat_history, name='chat_history'),
    path('send-message/', views.send_message, name='send_message'),
] 
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class AssistantSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    skill_name = models.CharField(max_length=100)
    learning_goal = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.skill_name}"

class AssistantChat(models.Model):
    session = models.ForeignKey(AssistantSession, on_delete=models.CASCADE)
    question = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.session.user.username} - {self.question[:50]}"

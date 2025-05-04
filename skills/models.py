from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Skill(models.Model):
    MODE_CHOICES = [
        ('teach', 'Teach'),
        ('learn', 'Learn'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    skill_name = models.CharField(max_length=100)
    description = models.TextField()
    mode = models.CharField(max_length=5, choices=MODE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'skill_name', 'mode')

    def __str__(self):
        return f"{self.user.username} - {self.skill_name} ({self.mode})"

    def get_matches(self):
        """Get users who want to learn if this user wants to teach, and vice versa."""
        opposite_mode = 'learn' if self.mode == 'teach' else 'teach'
        return Skill.objects.filter(
            skill_name=self.skill_name,
            mode=opposite_mode
        ).exclude(user=self.user)

class ChatMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['timestamp']
    
    def __str__(self):
        return f"{self.sender.username} to {self.receiver.username}: {self.content[:50]}"

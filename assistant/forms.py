from django import forms
from .models import AssistantSession, AssistantChat

class AssistantSessionForm(forms.ModelForm):
    class Meta:
        model = AssistantSession
        fields = ['skill_name', 'learning_goal']
        widgets = {
            'learning_goal': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'What would you like to achieve with this skill?'
            }),
        }

class AssistantChatForm(forms.ModelForm):
    class Meta:
        model = AssistantChat
        fields = ['question']
        widgets = {
            'question': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Ask your question here...'
            }),
        } 
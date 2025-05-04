from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .models import AssistantSession, AssistantChat
from .forms import AssistantSessionForm, AssistantChatForm
from skills.models import Skill

def mock_api_response(prompt):
    """Mock API response for demonstration purposes."""
    if 'roadmap' in prompt.lower():
        return """Here's a learning roadmap for you:
1. Start with the basics
2. Practice fundamental concepts
3. Work on small projects
4. Join online communities
5. Build a portfolio
6. Contribute to open source"""
    elif 'resources' in prompt.lower():
        return """Recommended resources:
1. Online courses: Coursera, edX
2. YouTube channels: Tutorial Channel
3. Books: Beginner's Guide
4. Practice websites: Practice Platform
5. Community forums: Stack Overflow"""
    else:
        return "I'm here to help you learn. What specific questions do you have about the topic?"

@login_required
def assistant_home(request):
    # Check if user has any unmatched skills for more than 2 days
    two_days_ago = timezone.now() - timedelta(days=2)
    unmatched_skills = Skill.objects.filter(
        user=request.user,
        created_at__lte=two_days_ago
    ).exclude(
        skill_name__in=Skill.objects.exclude(user=request.user).values('skill_name')
    )

    if not unmatched_skills.exists():
        messages.info(request, "The AI Assistant is available for skills that haven't found a match in 2 days.")
        return redirect('skill_list')

    sessions = AssistantSession.objects.filter(user=request.user).order_by('-created_at')
    
    if request.method == 'POST':
        form = AssistantSessionForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.user = request.user
            session.save()
            return redirect('assistant_chat', session_id=session.id)
    else:
        form = AssistantSessionForm()

    context = {
        'form': form,
        'sessions': sessions,
        'unmatched_skills': unmatched_skills
    }
    return render(request, 'assistant/home.html', context)

@login_required
def assistant_chat(request, session_id):
    session = get_object_or_404(AssistantSession, id=session_id, user=request.user)
    chats = AssistantChat.objects.filter(session=session)
    
    if request.method == 'POST':
        form = AssistantChatForm(request.POST)
        if form.is_valid():
            chat = form.save(commit=False)
            chat.session = session
            
            # Get API response (mocked for now)
            prompt = f"Skill: {session.skill_name}\nGoal: {session.learning_goal}\nQuestion: {chat.question}"
            chat.response = mock_api_response(prompt)
            
            chat.save()
            return redirect('assistant_chat', session_id=session_id)
    else:
        form = AssistantChatForm()

    context = {
        'session': session,
        'chats': chats,
        'form': form
    }
    return render(request, 'assistant/chat.html', context)

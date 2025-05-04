from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Skill, ChatMessage
from .forms import SkillForm
import requests
from django.conf import settings
from datetime import datetime, timezone
import json
import google.generativeai as genai
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from django.db import models

# Configure the Gemini API
genai.configure(api_key=settings.GEMINI_API_KEY)

@login_required
def skill_list(request):
    user_skills = Skill.objects.filter(user=request.user)
    context = {
        'teaching_skills': user_skills.filter(mode='teach'),
        'learning_skills': user_skills.filter(mode='learn')
    }
    return render(request, 'skills/skill_list.html', context)

@login_required
def add_skill(request):
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.user = request.user
            try:
                skill.save()
                messages.success(request, 'Skill added successfully!')
                return redirect('skill_list')
            except:
                messages.error(request, 'You already have this skill in this mode.')
    else:
        form = SkillForm()
    return render(request, 'skills/add_skill.html', {'form': form})

@login_required
def delete_skill(request, pk):
    skill = get_object_or_404(Skill, pk=pk, user=request.user)
    skill.delete()
    messages.success(request, 'Skill deleted successfully!')
    return redirect('skill_list')

@login_required
def matches(request):
    user_skills = Skill.objects.filter(user=request.user)
    matches = []
    
    for skill in user_skills:
        matched_skills = skill.get_matches()
        if matched_skills.exists():
            matches.append({
                'skill': skill,
                'matches': matched_skills
            })
    
    return render(request, 'skills/matches.html', {
        'matches': matches,
        'user_skills': user_skills
    })

@login_required
def ai_assistant(request):
    # Only get learning skills
    user_skills = Skill.objects.filter(user=request.user, mode='learn')
    selected_skill = None
    days_since_creation = None
    chat_history = []
    start_session = False
    
    # Get user-specific chat history
    chat_history = request.session.get(f'chat_history_{request.user.id}', [])
    
    # Handle skill selection
    skill_id = request.GET.get('skill_id') or request.POST.get('skill_id')
    if skill_id:
        selected_skill = get_object_or_404(Skill, id=skill_id, user=request.user, mode='learn')
        days_since_creation = (datetime.now(timezone.utc) - selected_skill.created_at).days
        
        # Check if user has confirmed to start session
        start_session = request.POST.get('start_session') == 'true'
        
        # Only generate AI response if:
        # 1. Skill is 2 days or older, OR
        # 2. User has confirmed to start session
        if days_since_creation >= 2 or start_session:
            # Clear chat history when starting new session
            chat_history = []
            request.session[f'chat_history_{request.user.id}'] = chat_history
            
            # Add initial prompt when skill is selected
            initial_prompt = f"""As an AI skill matching assistant, analyze the following skill and provide recommendations:

Skill: {selected_skill.skill_name}
Mode: {selected_skill.mode}
Description: {selected_skill.description}
Days since added: {days_since_creation}

Please provide:
1. Potential matches based on skill mode (teaching/learning)
2. Learning/teaching recommendations
3. Suggested next steps for skill development
4. Any relevant resources or communities

Format the response in a clear, structured way in a paragraph format having no bold text or other formatting and using simple day-to-day language."""
            
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(initial_prompt)
                chat_history.append({
                    'role': 'user',
                    'content': initial_prompt,
                    'timestamp': datetime.now().strftime('%H:%M')
                })
                chat_history.append({
                    'role': 'assistant',
                    'content': response.text,
                    'timestamp': datetime.now().strftime('%H:%M')
                })
                request.session[f'chat_history_{request.user.id}'] = chat_history
            except Exception as e:
                error_message = f"An error occurred: {str(e)}"
                messages.error(request, error_message)
                print(error_message)
    
    if request.method == 'POST':
        user_message = request.POST.get('user_message', '').strip()
        
        if user_message and selected_skill:
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # Prepare the context for the AI
                context = f"""You are a helpful AI assistant for SkillShelf, a skill-sharing platform. 
                The user is working with the following skill:
                Skill: {selected_skill.skill_name}
                Mode: {selected_skill.mode}
                Description: {selected_skill.description}
                Days since added: {days_since_creation}
                
                Previous conversation:
                {chr(10).join([f"{msg['role'].title()}: {msg['content']}" for msg in chat_history])}
                
                User's new message: {user_message}
                
                Please respond in a friendly, conversational way. Keep your responses concise and helpful. Remove any bold text or other formatting. Simulate a human response."""
                
                response = model.generate_content(context)
                chat_history.append({
                    'role': 'user',
                    'content': user_message,
                    'timestamp': datetime.now().strftime('%H:%M')
                })
                chat_history.append({
                    'role': 'assistant',
                    'content': response.text,
                    'timestamp': datetime.now().strftime('%H:%M')
                })
                request.session[f'chat_history_{request.user.id}'] = chat_history
                
            except Exception as e:
                error_message = f"An error occurred: {str(e)}"
                messages.error(request, error_message)
                print(error_message)
    
    return render(request, 'skills/ai_assistant.html', {
        'user_skills': user_skills,
        'selected_skill': selected_skill,
        'days_since_creation': days_since_creation,
        'chat_history': chat_history,
        'current_user': request.user.username,
        'start_session': start_session
    })

@login_required
def chat_history(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    messages = ChatMessage.objects.filter(
        (models.Q(sender=request.user, receiver=other_user) |
         models.Q(sender=other_user, receiver=request.user))
    ).order_by('timestamp')
    
    # Mark unread messages as read
    unread_messages = messages.filter(receiver=request.user, is_read=False)
    unread_messages.update(is_read=True)
    
    messages_data = [{
        'sender': message.sender.username,
        'content': message.content,
        'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M'),
        'is_sender': message.sender == request.user
    } for message in messages]
    
    return JsonResponse({'messages': messages_data})

@login_required
@require_http_methods(['POST'])
def send_message(request):
    try:
        data = json.loads(request.body)
        user_id = data.get('user_id')
        message_content = data.get('message')
        
        if not user_id or not message_content:
            return JsonResponse({'success': False, 'error': 'Missing required fields'})
        
        receiver = get_object_or_404(User, id=user_id)
        
        # Create new message
        message = ChatMessage.objects.create(
            sender=request.user,
            receiver=receiver,
            content=message_content
        )
        
        return JsonResponse({
            'success': True,
            'message': {
                'sender': message.sender.username,
                'content': message.content,
                'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M'),
                'is_sender': True
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

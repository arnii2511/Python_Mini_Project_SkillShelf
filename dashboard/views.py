from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from skills.models import Skill
from books.models import Book, BorrowRequest
from assistant.models import AssistantSession

@login_required
def dashboard(request):
    # Get user's skills
    teaching_skills = Skill.objects.filter(user=request.user, mode='teach')
    learning_skills = Skill.objects.filter(user=request.user, mode='learn')
    
    # Get skill matches
    matches = []
    for skill in Skill.objects.filter(user=request.user):
        skill_matches = skill.get_matches()
        if skill_matches.exists():
            matches.append({
                'skill': skill,
                'matches': skill_matches[:3]  # Limit to 3 matches
            })
    
    # Get user's books and requests
    books = Book.objects.filter(owner=request.user)
    incoming_requests = BorrowRequest.objects.filter(
        book__owner=request.user,
        status='pending'
    )
    outgoing_requests = BorrowRequest.objects.filter(
        requester=request.user
    ).exclude(status='returned')
    
    # Get recent AI assistant sessions
    assistant_sessions = AssistantSession.objects.filter(
        user=request.user
    ).order_by('-created_at')[:3]
    
    context = {
        'teaching_skills': teaching_skills,
        'learning_skills': learning_skills,
        'matches': matches,
        'books': books,
        'incoming_requests': incoming_requests,
        'outgoing_requests': outgoing_requests,
        'assistant_sessions': assistant_sessions
    }
    return render(request, 'dashboard/dashboard.html', context)

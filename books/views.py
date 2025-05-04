from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Book, BorrowRequest
from .forms import BookForm, BorrowRequestForm

@login_required
def book_list(request):
    query = request.GET.get('q', '')
    genre = request.GET.get('genre', '')
    availability = request.GET.get('availability', '')

    books = Book.objects.all().exclude(owner=request.user)

    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(description__icontains=query)
        )
    
    if genre:
        books = books.filter(genre=genre)
    
    if availability:
        is_available = availability == 'available'
        books = books.filter(is_available=is_available)

    context = {
        'books': books,
        'query': query,
        'genre': genre,
        'availability': availability,
        'genre_choices': Book.GENRE_CHOICES
    }
    return render(request, 'books/book_list.html', context)

@login_required
def my_books(request):
    books = Book.objects.filter(owner=request.user)
    return render(request, 'books/my_books.html', {'books': books})

@login_required
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.owner = request.user
            book.save()
            messages.success(request, 'Book added successfully!')
            return redirect('my_books')
    else:
        form = BookForm()
    return render(request, 'books/add_book.html', {'form': form})

@login_required
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    borrow_form = None
    user_request = None

    if request.user != book.owner:
        user_request = BorrowRequest.objects.filter(
            book=book,
            requester=request.user
        ).first()
        
        if not user_request and book.is_available:
            borrow_form = BorrowRequestForm()

    context = {
        'book': book,
        'borrow_form': borrow_form,
        'user_request': user_request
    }
    return render(request, 'books/book_detail.html', context)

@login_required
def borrow_request(request, pk):
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST' and book.is_available:
        form = BorrowRequestForm(request.POST)
        if form.is_valid():
            borrow_request = form.save(commit=False)
            borrow_request.book = book
            borrow_request.requester = request.user
            borrow_request.save()
            messages.success(request, 'Borrow request sent successfully!')
            return redirect('book_detail', pk=pk)
    
    return redirect('book_list')

@login_required
def manage_requests(request):
    # Incoming requests for my books
    incoming_requests = BorrowRequest.objects.filter(
        book__owner=request.user,
        status='pending'
    )
    
    # My outgoing requests
    outgoing_requests = BorrowRequest.objects.filter(
        requester=request.user
    )

    context = {
        'incoming_requests': incoming_requests,
        'outgoing_requests': outgoing_requests
    }
    return render(request, 'books/manage_requests.html', context)

@login_required
def handle_request(request, request_id, action):
    borrow_request = get_object_or_404(
        BorrowRequest,
        id=request_id,
        book__owner=request.user,
        status='pending'
    )
    
    if action == 'accept':
        borrow_request.accept()
        messages.success(request, 'Request accepted successfully!')
    elif action == 'reject':
        borrow_request.reject()
        messages.success(request, 'Request rejected successfully!')
    elif action == 'return':
        borrow_request.return_book()
        messages.success(request, 'Book marked as returned!')
    
    return redirect('manage_requests')

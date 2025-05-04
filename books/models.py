from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Book(models.Model):
    GENRE_CHOICES = [
        ('fiction', 'Fiction'),
        ('non-fiction', 'Non-Fiction'),
        ('science', 'Science'),
        ('technology', 'Technology'),
        ('history', 'History'),
        ('biography', 'Biography'),
        ('self-help', 'Self-Help'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    genre = models.CharField(max_length=20, choices=GENRE_CHOICES, default='other')
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_books')
    shared_with = models.ManyToManyField(User, related_name='shared_books', blank=True)
    is_available = models.BooleanField(default=True)
    is_donation = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book_detail', kwargs={'pk': self.pk})

    def get_active_request(self):
        return self.borrowrequest_set.filter(status='accepted').first()

class BorrowRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('returned', 'Returned'),
    ]

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='borrow_requests')
    request_message = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.requester.username} - {self.book.title}"

    def accept(self):
        self.status = 'accepted'
        self.book.is_available = False
        self.book.save()
        self.save()

    def reject(self):
        self.status = 'rejected'
        self.save()

    def return_book(self):
        self.status = 'returned'
        self.book.is_available = True
        self.book.save()
        self.save()

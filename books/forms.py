from django import forms
from .models import Book, BorrowRequest

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'genre', 'description', 'is_donation']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class BorrowRequestForm(forms.ModelForm):
    class Meta:
        model = BorrowRequest
        fields = ['request_message']
        widgets = {
            'request_message': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Please explain why you would like to borrow this book...'
            }),
        } 
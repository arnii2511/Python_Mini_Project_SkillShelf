from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('my-books/', views.my_books, name='my_books'),
    path('add/', views.add_book, name='add_book'),
    path('<int:pk>/', views.book_detail, name='book_detail'),
    path('<int:pk>/borrow/', views.borrow_request, name='borrow_request'),
    path('requests/', views.manage_requests, name='manage_requests'),
    path('requests/<int:request_id>/<str:action>/', views.handle_request, name='handle_request'),
] 
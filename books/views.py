from django.shortcuts import render, get_object_or_404
from .models import Book
from django.db.models import Q

def home(request):
    latest_books = Book.objects.order_by('-created_at')[:8]
    return render(request, 'books/home.html', {'latest_books': latest_books})


def book_search(request):
    query = request.GET.get('q', '')
    books = Book.objects.all()
    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(isbn__icontains=query)
        )
    return render(request, 'books/book_search.html', {'books': books, 'query': query})


def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'books/book_detail.html', {'book': book})

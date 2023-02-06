from django.shortcuts import render
from .models import Book, BookInstance, Author, Genre

# Create your views here.

def index(request):
    num_books = Book.objects.all().count()
    num_books_instance = BookInstance.objects.all().count()

    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()

    context = {
        'num_books': num_books,
        'num_books_instance': num_books_instance,
        'number_instances_available': num_instances_available,
        'num_authors': num_authors,
    }

    return render(request, 'index.html', context=context)

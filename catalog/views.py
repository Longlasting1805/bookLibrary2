from django.shortcuts import render
from .models import Book, BookInstance, Author, Genre
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
import datetime
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from catalog.forms import RenewBookForm
# Create your views here.

def index(request):
    num_books = Book.objects.all().count()
    num_books_instance = BookInstance.objects.all().count()

    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_books_instance': num_books_instance,
        'number_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
    }

    return render(request, 'index.html', context=context)

class BookListView(generic.ListView):
    model = Book
    context_object_name = 'book_list' 
    paginate_by = 2  

class BookDetailView(generic.DetailView):
    model = Book     

class AuthorListView(generic.ListView):
    model = Author  
    context_object_name = 'author_list'
      

class AuthorDetailView(generic.DetailView):
    model = Author    

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 2

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')
@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_liberian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk)

    if request.method == 'POST':
        form = RenewBookForm(request.POST)

        if form.is_valid():
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()
            return HttpResponseRedirect(reverse('all-borrowed'))

        else:
            proposed_renewal_date = date.datetime.today() + datetime.timedelta(weeks=3)
            form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

        context = {
            'form': form,
            'book_instance': book_instance,
        }

        return render(request, 'catalog/book_renew_liberian.html', context)        
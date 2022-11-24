from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import paginator
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView

from books.forms import ReviewCreateForm
from books.models import Book, Review


# class BookListView(ListView):
#     template_name = 'book_list.html'
#     queryset = Book.objects.all()
#     context_object_name = 'books'
#     paginate_by = 2


class BookListView(View):
    def get(self, request):
        books = Book.objects.all().order_by('id')
        search_query = request.GET.get('q', '')
        if search_query:
            books = books.filter(title__icontains=search_query)

        page_size = request.GET.get('page_size', 4)
        paginator = Paginator(books, page_size)
        
        page_num = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_num)

        return render(request, 'book_list.html', {'page_obj': page_obj, 'search_query': search_query})


# class BookDetailView(DetailView):
#     template_name = 'book_detail.html'
#     pk_url_kwarg = 'id'
#     model = Book

class BookDetailView(View):
    def get(self, request, id):
        book = Book.objects.get(id=id)
        review_form = ReviewCreateForm()
        return render(request, 'book_detail.html', {'book': book, 'review_form': review_form})


class AddReviewView(LoginRequiredMixin, View):
    def post(self, request, id):
        book = Book.objects.get(id=id)
        review_form = ReviewCreateForm(data=request.POST)

        if review_form.is_valid():
            Review.objects.create(
                book_id=book,
                user_id=request.user,
                stars_given=review_form.cleaned_data['stars_given'],
                review_text=review_form.cleaned_data['review_text']
            )
            return redirect(reverse('book_detail', kwargs={'id': book.id}))

        return render(request, 'book_detail.html', {'book': book, 'review_form': review_form})
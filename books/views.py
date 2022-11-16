from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView

from books.models import Book


class BookListView(ListView):
    template_name = 'book_list.html'
    queryset = Book.objects.all()
    context_object_name = 'books'


class BookDetailView(DetailView):
    template_name = 'book_detail.html'
    pk_url_kwarg = 'id'
    model = Book

# class BookListView(View):
#     def get(self, request):
#         books = Book.objects.all()
#
#         return render(request, 'book_list.html', {'books': books})

# class BookDetailView(View):
#     def get(self, request, id):
#         book = Book.objects.get(id=id)
#         return render(request, 'book_detail.html', {'book': book})

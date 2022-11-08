from django.shortcuts import render
from django.views import View

from books.models import Book


class BookListView(View):
    def get(self, request):
        books = Book.objects.all()

        return render(request, 'book_list.html', {'books': books})


class BookDetailView(View):
    def get(self, request, id):
        book = Book.objects.get(id=id)
        return render(request, 'book_detail.html', {'book': book})

from django.test import TestCase
from django.urls import reverse

from books.models import Book


class BookTestCase(TestCase):
    def test_no_books(self):
        response = self.client.get(reverse('book_list'))

        self.assertContains(response, 'No books found.')

    def test_book_list(self):
        book1 = Book.objects.create(title='Book1', description='Description1', isbn='12389744')
        book2 = Book.objects.create(title='Book2', description='Description2', isbn='32837812')
        book3 = Book.objects.create(title='Book3', description='Description3', isbn='44782829')

        response = self.client.get(reverse('book_list'))

        for book in [book1, book2]:
            self.assertContains(response, book.title)

        response = self.client.get(reverse('book_list') + '?page=2')
        self.assertContains(response, book3.title)

    def test_book_detail(self):
        book = Book.objects.create(title='Book1', description='Description1', isbn='12389744')

        response = self.client.get(reverse('book_detail', kwargs={'id': book.id}))
        self.assertContains(response, book.title)
        self.assertContains(response, book.description)

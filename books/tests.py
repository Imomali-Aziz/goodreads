from django.test import TestCase
from django.urls import reverse

from books.models import Book
from users.models import CustomUser


class BookTestCase(TestCase):
    def test_no_books(self):
        response = self.client.get(reverse('book_list'))

        self.assertContains(response, 'No books found.')

    def test_book_list(self):
        book1 = Book.objects.create(title='Book1', description='Description1', isbn='12389744')
        book2 = Book.objects.create(title='Book2', description='Description2', isbn='32837812')
        book3 = Book.objects.create(title='Book3', description='Description3', isbn='44782829')

        response = self.client.get(reverse('book_list') + '?page_size=2')

        for book in [book1, book2]:
            self.assertContains(response, book.title)
        self.assertNotContains(response, book3.title)

        response = self.client.get(reverse('book_list') + '?page=2&page_size=2')
        self.assertContains(response, book3.title)

    def test_book_detail(self):
        book = Book.objects.create(title='Book1', description='Description1', isbn='12389744')

        response = self.client.get(reverse('book_detail', kwargs={'id': book.id}))
        self.assertContains(response, book.title)
        self.assertContains(response, book.description)

    def test_book_search(self):
        book1 = Book.objects.create(title='skateboard', description='Description1', isbn='12389744')
        book2 = Book.objects.create(title='cat', description='Description2', isbn='32837812')
        book3 = Book.objects.create(title='macbook', description='Description3', isbn='44782829')

        response = self.client.get(reverse('book_list') + '?q=skateboard')
        self.assertContains(response, book1.title)
        self.assertNotContains(response, book2.title)
        self.assertNotContains(response, book3.title)

        response = self.client.get(reverse('book_list') + '?q=cat')
        self.assertContains(response, book2.title)
        self.assertNotContains(response, book1.title)
        self.assertNotContains(response, book3.title)

        response = self.client.get(reverse('book_list') + '?q=macbook')
        self.assertContains(response, book3.title)
        self.assertNotContains(response, book1.title)
        self.assertNotContains(response, book2.title)


class ReviewTestCase(TestCase):
    def test_add_review(self):
        book = Book.objects.create(title='Book1', description='Description1', isbn='12389744')
        user = CustomUser.objects.create_user(username='test_user', first_name='Test', last_name='User',
                                              email='test@user.com')
        user.set_password('somepassword')
        user.save()

        self.client.login(username='test_user', password='somepassword')

        self.client.post(reverse('book_review', kwargs={'id': book.id}), data={
            'stars_given': 4,
            'review_text': 'Amazing book'
        })
        reviews = book.review_set.all()

        self.assertEqual(reviews.count(), 1)
        self.assertEqual(reviews[0].stars_given, 4)
        self.assertEqual(reviews[0].review_text, 'Amazing book')
        self.assertEqual(reviews[0].book_id, book)
        self.assertEqual(reviews[0].user_id, user)



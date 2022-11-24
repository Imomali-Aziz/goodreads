from django.test import TestCase
from django.urls import reverse

from books.models import Book, Review
from users.models import CustomUser


class HomePageTestCase(TestCase):
    def test_all_reviews(self):
        book = Book.objects.create(title='Book1', description='Description1', isbn='12389744')
        user = CustomUser.objects.create_user(username='test_user', first_name='Test', last_name='User',
                                              email='test@user.com')
        user.set_password('somepassword')
        user.save()

        review1 = Review.objects.create(review_text='Nice book', stars_given='3', user_id=user, book_id=book)
        review2 = Review.objects.create(review_text='Amazing book', stars_given='4', user_id=user, book_id=book)
        review3 = Review.objects.create(review_text='Loved this book', stars_given='5', user_id=user, book_id=book)

        response = self.client.get(reverse('home_page') + '?page_size=2&page_num=1')

        self.assertContains(response, review3.review_text)
        self.assertContains(response, review2.review_text)
        self.assertNotContains(response, review1.review_text)

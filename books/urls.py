from django.urls import path

from books.views import BookListView, BookDetailView, AddReviewView

urlpatterns = [
    path('', BookListView.as_view(), name='book_list'),
    path('<int:id>/', BookDetailView.as_view(), name='book_detail'),
    path('<int:id>/reviews/', AddReviewView.as_view(), name='book_review'),
]
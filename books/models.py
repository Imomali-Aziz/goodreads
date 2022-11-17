from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from users.models import CustomUser


class Book(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    isbn = models.CharField(max_length=17)
    cover_picture = models.ImageField(default='default_cover.webp')

    def __str__(self):
        return self.title
    

class Author(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    bio = models.TextField()
    email = models.EmailField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class BookAuthor(models.Model):
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    author_id = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.book_id.title} by {self.author_id.first_name} {self.author_id.last_name}"


class Review(models.Model):
    review_text = models.TextField()
    stars_given = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.stars_given} stars given to {self.book_id.title} from {self.user_id.username}"

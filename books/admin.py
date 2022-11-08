from django.contrib import admin
from .models import Book, Author, BookAuthor, Review


class BookAdmin(admin.ModelAdmin):
    search_fields = ('title', 'description')
    list_display = ('title', 'description', 'isbn')


class AuthorAdmin(admin.ModelAdmin):
    search_fields = ('first_name', 'last_name', 'email')
    list_display = ('first_name', 'last_name', 'email')


class BookAuthorAdmin(admin.ModelAdmin):
    search_fields = ('book_id', 'author_id')


class ReviewAdmin(admin.ModelAdmin):
    search_fields = ('review_text',)
    list_filter = ('stars_given',)


admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(BookAuthor, BookAuthorAdmin)
admin.site.register(Review, ReviewAdmin)

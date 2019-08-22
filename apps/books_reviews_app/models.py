from django.db import models
from apps.login_registration_app.models import *

class BookManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}

        if len(postData['title']) < 2:
            errors['title'] = "Book Title must be longer than 2 characters"
        if len(postData['add_author']) <2:
            errors['add_author'] = "Author Name must be longer than 2 characters"

        return errors

class ReviewManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}

        if len(postData['review']) < 5:
            errors['review'] = "Review must be longer than 5 characters"

        return errors

# Create your models here.

class Author(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return f"<Author object: {self.id}>"

class Book(models.Model):
    title = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(Author, related_name="books")
    objects = BookManager()

    def __repr__(self):
        return f"<Book object: {self.id}>"

class Review(models.Model):
    review = models.TextField()
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    book = models.ForeignKey(Book, related_name="reviews")
    user = models.ForeignKey(User, related_name="reviews")
    objects = ReviewManager()

    def __repr__(self):
        return f"<Review object: {self.id}>"

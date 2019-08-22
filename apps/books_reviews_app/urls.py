from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^books$', views.books_home),
    url(r'^books/(?P<book_id>[0-9]+)$', views.display_book),
    url(r'^users/(?P<user_id>[0-9]+)$', views.display_user),
    url(r'^books/add$', views.display_add),
    url(r'^add_book$', views.add_book_and_review),
    url(r'^add_review$', views.add_review),
    url(r'^delete_review$', views.delete_review),
]
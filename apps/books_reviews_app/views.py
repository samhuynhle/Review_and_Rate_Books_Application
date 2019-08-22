from django.shortcuts import render, redirect
from .models import *
from apps.login_registration_app.models import *
from django.contrib import messages

from datetime import date, datetime, timezone

# Create your views here.
def books_home(request):
    if 'user_id' not in request.session or request.session['user_id'] == 'logged out':
        request.session['user_id'] = 'logged out'
        return redirect('/')

    recent_reviews = []
    recent_reviews_ratings = []
    all_reviews = Review.objects.all().order_by('-created_at')
    
    if len(all_reviews) > 0:
        review_one = all_reviews[0]
        review_one_stars = []
        for i in range(review_one.rating):
            review_one_stars.append('gold')
        for i in range(5-review_one.rating):
            review_one_stars.append('silver')
        review_one_stars.append(all_reviews[0])
        recent_reviews.append(all_reviews[0])


    if len(all_reviews) > 1:
        review_two = all_reviews[1]
        review_two_stars = []
        for i in range(review_two.rating):
            review_two_stars.append('gold')
        for i in range(5-review_two.rating):
            review_two_stars.append('silver')
        review_two_stars.append(all_reviews[1])
        recent_reviews.append(all_reviews[1])


    if len(all_reviews) > 2:
        review_three = all_reviews[2]
        review_three_stars = []
        for i in range(review_three.rating):
            review_three_stars.append('gold')
        for i in range(5-review_three.rating):
            review_three_stars.append('silver')
        review_three_stars.append(all_reviews[2])
        recent_reviews.append(all_reviews[2])



    context = {
        'all_books': Book.objects.all(),
        'current_user': User.objects.get(id=request.session['user_id']),
        'recent_reviews': recent_reviews,
        'review_one_stars': review_one_stars,
        'review_two_stars': review_two_stars,
        'review_three_stars': review_three_stars,
    }

    return render(request, 'books_reviews_app/books_reviews_home.html', context)

def display_book(request, book_id):
    if 'user_id' not in request.session or request.session['user_id'] == 'logged out':
        request.session['user_id'] = 'logged out'
        return redirect('/')

    recent_reviews = []
    recent_reviews_ratings = []
    all_reviews = Review.objects.all().order_by('-created_at')
    request.session['current_book'] = book_id
    
    if len(all_reviews) > 0:
        review_one = all_reviews[0]
        review_one_stars = []
        for i in range(review_one.rating):
            review_one_stars.append('gold')
        for i in range(5-review_one.rating):
            review_one_stars.append('silver')
        review_one_stars.append(all_reviews[0])
        recent_reviews.append(all_reviews[0])


    if len(all_reviews) > 1:
        review_two = all_reviews[1]
        review_two_stars = []
        for i in range(review_two.rating):
            review_two_stars.append('gold')
        for i in range(5-review_two.rating):
            review_two_stars.append('silver')
        review_two_stars.append(all_reviews[1])
        recent_reviews.append(all_reviews[1])


    if len(all_reviews) > 2:
        review_three = all_reviews[2]
        review_three_stars = []
        for i in range(review_three.rating):
            review_three_stars.append('gold')
        for i in range(5-review_three.rating):
            review_three_stars.append('silver')
        review_three_stars.append(all_reviews[2])
        recent_reviews.append(all_reviews[2])



    context = {
        'current_book': Book.objects.get(id=book_id),
        'current_user': User.objects.get(id=request.session['user_id']),
        'recent_reviews': recent_reviews,
        'review_one_stars': review_one_stars,
        'review_two_stars': review_two_stars,
        'review_three_stars': review_three_stars,
    }

    return render(request, 'books_reviews_app/display_book.html', context)

def display_user(request, user_id):
    if 'user_id' not in request.session or request.session['user_id'] == 'logged out':
        request.session['user_id'] = 'logged out'
        return redirect('/')

    current_user = User.objects.get(id=request.session['user_id'])

    reviewed_books_list = []

    for review in current_user.reviews.all():
        reviewed_books_list.append(review.book)

    context = {
        'current_user': current_user,
        'total_reviews': len(current_user.reviews.all()),
        'reviewed_books_list': reviewed_books_list,
    }

    return render(request, 'books_reviews_app/display_user.html', context)

def display_add(request):
    if 'user_id' not in request.session or request.session['user_id'] == 'logged out':
        request.session['user_id'] = 'logged out'
        return redirect('/')

    context = {
        'current_user': User.objects.get(id=request.session['user_id']),
        'all_authors': Author.objects.all()
    }
    return render(request, 'books_reviews_app/add_book.html', context)

def add_book_and_review(request):
    if 'user_id' not in request.session or request.session['user_id'] == 'logged out':
        request.session['user_id'] = 'logged out'
        return redirect('/')

    current_user = User.objects.get(id=request.session['user_id'])

    #Validation for Bokk
    errors = Book.objects.basic_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request,value)

    errors = Review.objects.basic_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request,value)
        return redirect('/books/add')


    if len(request.POST['add_author']) > 0:
        new_author = Author.objects.create(name=request.POST['add_author'])
        new_book = Book.objects.create(title=request.POST['title'], author = new_author)        
        new_book.save()
        new_author.save()
    else:
        selected_author = Author.objects.get(id=request.POST['select_author'])
        new_book = Book.objects.create(title=request.POST['title'], author = selected_author)

    
    new_review = Review.objects.create(review=request.POST['review'], rating=request.POST['rating'], book=new_book, user=current_user)
    new_review.save()

    request.session['current_book'] = new_book.id
    return redirect(f"/books/{new_book.id}")

def add_review(request):
    if 'user_id' not in request.session or request.session['user_id'] == 'logged out':
        request.session['user_id'] = 'logged out'
        return redirect('/')

    current_book = Book.objects.get(id=request.session['current_book'])
    errors = Review.objects.basic_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request,value)
        return redirect(f'/books/{current_book.id}')
    else:
        if 'user_id' not in request.session or request.session['user_id'] == 'logged out':
            request.session['user_id'] = 'logged out'
            return redirect('/')

        if 'current_book' not in request.session:
            return redirect('/')
        
        current_user = User.objects.get(id=request.session['user_id'])


        new_review = Review.objects.create(review=request.POST['review'], rating=request.POST['rating'], book= current_book, user=current_user)
        new_review.save()

        return redirect(f"/books/{current_book.id}")

def delete_review(request):
    if 'user_id' not in request.session or request.session['user_id'] == 'logged out':
        request.session['user_id'] = 'logged out'
        return redirect('/')

    if 'current_book' not in request.session:
        return redirect('/')

    current_user = User.objects.get(id=request.session['user_id'])
    current_book = Book.objects.get(id=request.session['current_book'])
    current_review = Review.objects.get(id=request.POST['review_id'])

    if current_review.user.id != current_user.id:
        return redirect('/')
    else:
        current_review.delete()
        return redirect(f"/books/{current_book.id}")


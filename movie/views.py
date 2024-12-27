from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponseNotFound, HttpResponseForbidden, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .models import movie,category,Review
from .forms import  movieform,ReviewForm
from django.core.paginator import Paginator,EmptyPage,InvalidPage
app_name='movie'
# Create your views here.
def index(request):
    return render(request,'index.html')

def allmoviecat(request,c_slug=None):
    categories = category.objects.all()
    c_page=None
    movies_list=None

    if c_slug !=None:
        c_page=get_object_or_404(category,slug=c_slug)
        movies_list=movie.objects.all().filter(category=c_page)
    else:
        movies_list=movie.objects.all().filter()
    paginator=Paginator(movies_list,4)
    try:
        page=int(request.GET.get('page',1))
    except:
        page=1
    try:
        movies=paginator.page(page)
    except (EmptyPage,InvalidPage):
        movies=paginator.page(paginator.num_pages)


    return render(request,"category.html",{'category':c_page,'movies':movies,'categories':categories})


def movie_show(request):
    movie_list = movie.objects.all()
    paginator = Paginator(movie_list, 4)  # Assuming you want 10 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'moviepage.html', context)


def add_movie(request):
    if request.method == 'POST':
        form = movieform(request.POST, request.FILES)
        if form.is_valid():
            movie_instance = form.save(commit=False)
            movie_instance.user = request.user  # Associate the movie with the logged-in user
            movie_instance.save()
            return redirect('movie:movie_show')  # Redirect to the movie listing page after adding the movie
    else:
        form = movieform()
    return render(request, 'add.html', {'form': form})

@login_required
def update(request, movie_id):
    movie_instance = get_object_or_404(movie, id=movie_id)
    if not movie_instance.can_be_modified_or_deleted_by(request.user):
        return HttpResponseForbidden("You don't have permission to update this movie.")
    if request.method == 'POST':
        form = movieform(request.POST, instance=movie_instance)
        if form.is_valid():
            form.save()
            return redirect('movie:detail', movie_id=movie_id)
    else:
        form = movieform(instance=movie_instance)
    return render(request, 'edit.html', {'form': form, 'movie': movie_instance})

@login_required
def delete(request, movie_id):
    movie_instance = get_object_or_404(movie, id=movie_id)
    if not movie_instance.can_be_modified_or_deleted_by(request.user):
        return HttpResponseForbidden("You don't have permission to delete this movie.")
    if request.method == 'POST':
        movie_instance.delete()
        return redirect('movie:movie_show')
    return render(request, 'delete.html', {'movie': movie_instance})
def detail(request, movie_id):
    movie_instance = get_object_or_404(movie, id=movie_id)
    reviews = Review.objects.filter(movie=movie_instance)
    form = ReviewForm()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.movie = movie_instance
            review.user = request.user
            review.save()
            return redirect('movie:detail', movie_id=movie_id)
        else:
            form = ReviewForm()

    return render(request, "details.html", {'movie': movie_instance,'reviews':reviews,'form':form})


def check_data_integrity(request):
    # Get all unique usernames from the movie table
    usernames = movie.objects.values_list('username', flat=True).distinct()

    # Get all unique user IDs from the auth_user table
    user_ids = User.objects.values_list('id', flat=True)

    # Identify discrepancies
    discrepancies = set(usernames) - set(user_ids)

    if discrepancies:
        message = f"Discrepancies found: {discrepancies}"
    else:
        message = "No discrepancies found."

    return render(request, 'data_integrity_check.html', {'message': message})
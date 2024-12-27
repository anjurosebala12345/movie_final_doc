from django.shortcuts import render
from movie.models import movie,category
from django.db.models import Q

def searchresult(request):
    movies = None
    query = None
    category_name = None

    if 'category' in request.GET:
        category_name = request.GET.get('category')

    if 'q' in request.GET:
        query = request.GET.get('q')
        movies = movie.objects.filter(Q(name__icontains=query) | Q(desc__icontains=query))

        if category_name:
            movies = movies.filter(category__name__icontains=category_name)

    print("Category Name:", category_name)
    print("Movies:", movies)

    return render(request, 'search.html', {'query': query, 'movies': movies})
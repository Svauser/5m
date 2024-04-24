from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Movie,Director,Review
from .serializers import DirectorSerializer, MovieSerializer, ReviewSerializer
from django.db.models import Avg, Count
# Create your views here.
@api_view(['GET'])
def director_list(request):
    directors = Director.objects.all()
    serializer = DirectorSerializer(directors, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def director_detail(request, id):
    try:
        director = Director.objects.get(id=id)
    except Director.DoesNotExist:
        return Response(data={'error':'Режиссер не найден!'},
                        status=status.HTTP_404_NOT_FOUND)
    serializer = DirectorSerializer(director,many=False)
    return Response(serializer.data)

@api_view(['GET'])
def movie_list(request):
    movies = Movie.objects.all()
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)
@api_view(['GET'])
def movie_detail(request, id):
    try:
        movie = Movie.objects.get(id=id)
        serializer = MovieSerializer(movie)
        return Response(serializer.data)
    except Movie.DoesNotExist:
        return Response(data={'error': 'Фильм не найден!'},
                        status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def review_list(request):
    reviews = Review.objects.all()
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def review_detail(request, id):
    try:
        review = Review.objects.get(id=id)
        serializer = ReviewSerializer(review)
        return Response(serializer.data)
    except Review.DoesNotExist:
        return Response(data={'error': 'Отзыв не найден!'},
                        status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def movie_reviews(request):
    movies = Movie.objects.prefetch_related('reviews')
    serializer = MovieSerializer(movies, many=True)

    average_ratings = {}

    for movie in movies:
        avg_rating = movie.reviews.aggregate(Avg('star'))['star__avg']
        average_ratings[movie.id] = avg_rating

    response_data = {
        'movies_with_reviews': serializer.data,
        'average_ratings': average_ratings
    }
    return Response(response_data)


@api_view(['GET'])
def director_list_with_movies_count(request):
    directors = Director.objects.all()
    serialized_directors = []

    for director in directors:
        movie_count = director.movie_set.count()
        serialized_director = {
            'id': director.id,
            'name': director.name,
            'movies_count': movie_count
        }
        serialized_directors.append(serialized_director)

    return Response(serialized_directors)


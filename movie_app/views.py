from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Movie,Director,Review
from .serializers import DirectorSerializer, MovieSerializer, ReviewSerializer
from django.db.models import Avg, Count
# Create your views here.
@api_view(['GET','POST'])
def director_list(request):
    if request.method == 'GET':
        directors = Director.objects.all()
        serializer = DirectorSerializer(directors, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        name=request.data.get('name')
        director=Director.objects.create(name=name)
        return Response(data={'director_id':director_id},status=status.HTTP_201_CREATED)
@api_view(['GET','PUT','DELETE'])
def director_detail(request, id):
    try:
        director = Director.objects.get(id=id)
    except Director.DoesNotExist:
        return Response(data={'error':'Режиссер не найден!'},
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = DirectorSerializer(director,many=False)
        return Response(serializer.data)
    elif request.method == 'PUT':
       director.name = request.data.get('name')
       director.save()
       return Response(data=DirectorSerializer(director).data,
                       status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        director.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET','POST'])
def movie_list(request):
    if request.method == 'GET':
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        title = request.data.get('title')
        description = request.data.get('description')
        duration = request.data.get('duration')
        director_id = request.data.get('director_id')
        movie = Movie.objects.create(title=title,
                                     description=description,
                                     duration=duration,
                                     director_id=director_id
                                     )
        return Response(data={'movie_id': movie_id}, status=status.HTTP_201_CREATED)
@api_view(['GET','PUT','DELETE'])
def movie_detail(request, id):
    try:
        movie = Movie.objects.get(id=id)
    except Movie.DoesNotExist:
        return Response(data={'error': 'Фильм не найден!'},
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = MovieSerializer(movie)
        return Response(serializer.data)
    elif request.method == 'PUT':
       movie.title = request.data.get('title')
       movie.description = request.data.get('description')
       movie.duration = request.data.get('duration')
       movie.director_id = request.data.get('director_id')
       movie.save()
       return Response(data=MovieSerializer(movie).data,
                       status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET','POST'])
def review_list(request):
    if request.method == 'GET':
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        text = request.data.get('text')
        star = request.data.get('star')
        movie_id = request.data.get('movie_id')
        review = Review.objects.create(text=text,
                                     star=star,
                                     movie_id=movie_id
                                     )
        return Response(data={'review_id': review_id}, status=status.HTTP_201_CREATED)

@api_view(['GET','PUT','DELETE'])
def review_detail(request, id):
    try:
        review = Review.objects.get(id=id)
        serializer = ReviewSerializer(review)
        return Response(serializer.data)
    except Review.DoesNotExist:
        return Response(data={'error': 'Отзыв не найден!'},
                        status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ReviewSerializer(review)
        return Response(serializer.data)
    elif request.method == 'PUT':
       review.text = request.data.get('text')
       reivew.star = request.data.get('star')
       reivew.movie_id = request.data.get('movie_id')
       review.save()
       return Response(data=ReviewSerializer(review).data,
                       status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
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



from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Movie,Director,Review
from .serializers import DirectorSerializer, MovieSerializer, ReviewSerializer,\
    MovieValidateSerializer,ReviewValidateSerializer,DirectorValidateSerializer
from django.db.models import Avg, Count
# Create your views here.
@api_view(['GET','POST'])
def director_list(request):
    if request.method == 'GET':
        directors = Director.objects.all()
        serializer = DirectorSerializer(directors, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        seralizer = DirectorValidateSerializer(data=request.data)
        if not seralizer.is_valid():
            return Response(data={'errors': seralizer.errors}, status=status.HTTP_406_NOT_ACCEPTABLE)
        name=serializer.validated_data.get('name')
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
       seralizer = DirectorValidateSerializer(data=request.data)
       seralizer.is_valid(raise_exeption=True)
       director.name = serializer.validated_data.get('name')
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
        seralizer=MovieValidateSerializer(data=request.data)
        if not seralizer.is_valid():
            return Response(data={'errors':seralizer.errors},status=status.HTTP_406_NOT_ACCEPTABLE)

        title = serializer.validated_data.get('title')
        description = serializer.validated_data.get('description')
        duration = serializer.validated_data.get('duration')
        director_id = serializer.validated_data.get('director_id')
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
       seralizer = MovieValidateSerializer(data=request.data)
       seralizer.is_valid(raise_exeption=True)
       movie.title = serializer.validated_data.get('title')
       movie.description = serializer.validated_data.get('description')
       movie.duration = serializer.validated_data.get('duration')
       movie.director_id = serializer.validated_data.get('director_id')
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
        seralizer = ReviewValidateSerializer(data=request.data)
        if not seralizer.is_valid():
            return Response(data={'errors': seralizer.errors}, status=status.HTTP_406_NOT_ACCEPTABLE)
        text = serializer.validated_data.get('text')
        star = serializer.validated_data.get('star')
        movie_id = serializer.validated_data.get('movie_id')
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
       seralizer = MovieValidateSerializer(data=request.data)
       seralizer.is_valid(raise_exeption=True)
       review.text = serializer.validated_data.get('text')
       reivew.star = serializer.validated_data.get('star')
       reivew.movie_id = serializer.validated_data.get('movie_id')
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



from rest_framework import serializers
from .models import Movie,Director,Review
from rest_framework.exceptions import ValidationError
class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = '__all__'

class MovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = 'id title description director duration reviews'.split()
        depth = 1
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class MovieValidateSerializer(serializers.Serializer):
    title=serializers.CharField(max_length=255,min_length=3)
    description=serializers.CharField(required=False)
    duration=serializers.IntegerField(max_value=1000)
    director_id=serializers.IntegerField(min_value=1)
    def validate_director_id(self,director_id):
        try:
            Director.objects.get(id=director_id)
        except Director.DoesNotExist:
            raise ValidationError('Director not found!')
        return director_id

class ReviewValidateSerializer(serializers.Serializer):
    text=serializers.CharField()
    star=serializers.IntegerField(min_value=1,max_value=5)
    movie_id=serializers.IntegerField(min_value=1)
    def validate_movie_id(self,movie_id):
        try:
            Director.objects.get(id=movie_id)
        except Director.DoesNotExist:
            raise ValidationError('Movie not found!')
        return movie_id

class DirectorValidateSerializer(serializers.Serializer):
    name=serializers.CharField()

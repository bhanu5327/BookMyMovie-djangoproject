from rest_framework import serializers
from BookMyMovie.models import *

class LocationsListSerializer(serializers.ModelSerializer):
    class Meta:
        model=Locations
        fields='__all__'

        def create(self, validated_data):
            """
            Create and return a new `Snippet` instance, given the validated data.
            """
            return Locations.objects.create(**validated_data)

        def update(self, instance, validated_data):

            """
            Update and return an existing `Snippet` instance, given the validated data.
            """

            instance.LocationName = validated_data.get('LocationName', instance.LocationName)

            instance.save()
            return instance


class MoviesListSerializer(serializers.ModelSerializer):
    class Meta:
        model=Movies
        fields=('id','MovieName','MoviePoster','MovieRating','Language','Genre','Location_id')

        def create(self, validated_data):
            """
            Create and return a new `Snippet` instance, given the validated data.
            """
            return Movies.objects.create(**validated_data)

        def update(self, instance, validated_data):

            """
            Update and return an existing `Snippet` instance, given the validated data.
            """

            instance.MovieName = validated_data.get('MovieName', instance.MovieName)
            instance.MoviePoster = validated_data.get('MoviePoster', instance.MoviePoster)
            instance.MovieRating = validated_data.get('MovieRating', instance.MovieRating)
            instance.Language = validated_data.get('Language', instance.Language)
            instance.Genre = validated_data.get('Genre', instance.Genre)

            instance.save()
            return instance

class TheatresListSerializer(serializers.ModelSerializer):
    class Meta:
        model=Theatres
        fields=('TheatreName','TheatreAddress','TheatreRating','Location_id','Movie_id')

        def create(self, validated_data):
            """
            Create and return a new `Snippet` instance, given the validated data.
            """
            return Theatres.objects.create(**validated_data)

        def update(self, instance, validated_data):

            """
            Update and return an existing `Snippet` instance, given the validated data.
            """

            instance.TheatreName = validated_data.get('TheatreName', instance.TheatreName)
            instance.TheatreAddress = validated_data.get('TheatreAddress', instance.TheatreAddress)
            instance.TheatreRating = validated_data.get('TheatreRating', instance.TheatreRating)


            instance.save()
            return instance



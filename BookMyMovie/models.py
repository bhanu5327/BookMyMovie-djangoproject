from django.db import models

from django.contrib.auth.models import User

# Create your models here.
class UserInfo(models.Model):
    User=models.ForeignKey(User, on_delete=models.CASCADE)
    Photo=models.ImageField(upload_to='images/',null=True,blank=True)
    Wallet=models.IntegerField(blank=True)

class Locations(models.Model):
    LocationName = models.CharField(max_length=50)


class Movies(models.Model):
    MovieName = models.CharField(max_length=50)
    MoviePoster=models.ImageField(upload_to='images/',blank=True,null=True)
    MovieRating = models.CharField(max_length=50)
    Language = models.CharField(max_length=50)
    Genre = models.CharField(max_length=50)
    trailer=models.CharField(max_length=100,blank=True)
    Location=models.ForeignKey(Locations, on_delete=models.CASCADE)


class Theatres(models.Model):
    TheatreName = models.CharField(max_length=50)
    TheatreAddress=models.CharField(max_length=200)
    TheatreRating = models.IntegerField()
    Movie = models.ForeignKey(Movies, on_delete=models.CASCADE)
    Location = models.ForeignKey(Locations, on_delete=models.CASCADE)


class SeatsInfo(models.Model):
    SeatNumber=models.CharField(max_length=50)
    SeatCost=models.IntegerField()
    MovieDate=models.DateField(default=True)
    MovieTime=models.CharField(max_length=50)
    BookedDateTime=models.DateTimeField(default=True)
    User=models.ForeignKey(User, on_delete=models.CASCADE)
    Theatre = models.ForeignKey(Theatres, on_delete=models.CASCADE)

class Reviews(models.Model):
    Movie=models.ForeignKey(Movies, on_delete=models.CASCADE)
    Review = models.CharField(max_length=200)



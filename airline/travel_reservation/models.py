from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):    #yaane traveler bel class diagram
    receive_promotions = models.BooleanField(
        default=False
    )
    birthdate = models.DateField(
        null=True,blank=True
    )


class Hotel(models.Model): #bss naamoul extend la models.Model , django bi sir fio yaamoul interaction maa l database
    #ma hatayna id la2n django automatically bye5la2la id lal class
    name = models.CharField( max_length=40)
    rating = models.DecimalField(decimal_places=1,max_digits=2)


class Room(models.Model):
    capacity = models.IntegerField()
    price = models.DecimalField(max_digits=4)
    number = models.IntegerField()
    hotel = models.ForeignKey(Hotel,on_delete=models.CASCADE)


class Airline(models.Model):
    name = models.CharField(max_length=40)

class AirPort(models.Model):
    name = models.CharField(max_length=40)

class Flight(models.Model):
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    is_Refundable = models.BooleanField()
    airport_from = models.ForeignKey(AirPort,on_delete=models.CASCADE ,related_name="departure")    
    airport_to = models.ForeignKey(AirPort,on_delete=models.CASCADE ,related_name="arrival")

class Country(models.Model):
    name = models.CharField()

class City(models.Model):
    name = models.CharField()   

class Booking(models.Model):
    date=models.DateField()
    cost=models.DecimalField()  #lezim zabeta hay champ calcule
    cancel_date=models.DateField()

class RoomBooKed(models.Model):
    room = models.ForeignKey(Room,on_delete=models.CASCADE)
    booking=models.ForeignKey(Booking,on_delete=models.CASCADE)

class Payment(models.Model):
    amount=models.DecimalField()
    date=models.DecimalField()











    
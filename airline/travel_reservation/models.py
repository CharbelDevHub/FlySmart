from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.forms import ValidationError
from django.utils import timezone
from datetime import timedelta
# Create your models here.


class User(AbstractUser):    #yaane traveler bel class diagram
    class Meta:
        db_table = 'User'
        
    receive_promotions = models.BooleanField(
        default=False
    )
    birthdate = models.DateField(
        null=True,blank=True
    )

class Airline(models.Model):
    class Meta:
        db_table = 'Airline'
    name = models.CharField(max_length=40)
    logo = models.URLField(null=True)

    def __str__(self) -> str:
        return f'{self.name}'

class Airplane_type(models.Model):
    class Meta:
        db_table = 'Airplane_Type'
    model = models.CharField(max_length=40,unique=True)
    capacity = models.IntegerField(null=True)

    def __str__(self) -> str:
        return f'{self.model}'
    
class Airplane(models.Model):
    class Meta:
        db_table = 'Airplane'
    code = models.CharField(max_length=40,unique=True,blank=True)    
    airline = models.ForeignKey(Airline,on_delete=models.CASCADE)    
    type = models.ForeignKey(Airplane_type,on_delete=models.CASCADE,null=True)

    def __str__(self) -> str:
        return f'{self.code}({self.airline})'
    
class Country(models.Model):
    class Meta:
        db_table = 'Country'
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f'{self.name}'

class City(models.Model):
    class Meta:
        db_table = 'City'
    name = models.CharField(max_length=40)
    image = models.URLField(null=True, blank=True)
    country = models.ForeignKey(Country,on_delete=models.CASCADE,null=True,blank=True)   

    def __str__(self) -> str:
        return f'{self.name}'

class Hotel(models.Model): #bss naamoul extend la models.Model , django bi sir fio yaamoul interaction maa l database
    #ma hatayna id la2n django automatically bye5la2la id lal class
    class Meta:
        db_table = 'Hotel'
    name = models.CharField(max_length=40)
    rating = models.DecimalField(decimal_places=1,max_digits=2)
    image = models.URLField()
    city = models.ForeignKey(City,on_delete=models.CASCADE)
    description=models.TextField(null=True,blank=True)

class Room(models.Model):
    ROOM_CATEGORIES = [
        ('standard', 'Standard Room'),  #first is how is stored in db , second is what the user sees
        ('deluxe', 'Deluxe Room'),
        ('suite', 'Suite'),
        ('executive', 'Executive Room'),
        ('family', 'Family Room'),
        ('junior_suite', 'Junior Suite'),
        ('connecting', 'Connecting Rooms'),
        ('honeymoon', 'Honeymoon Suite'),
        ('penthouse', 'Penthouse Suite'),
        ('accessible', 'Accessible Room'),
    ]
    class Meta:
        db_table = 'Room'
    capacity = models.IntegerField()
    price = models.DecimalField(max_digits=5,decimal_places=1)
    number = models.IntegerField()
    image = models.URLField()
    category = models.CharField(max_length=20,null=True,blank=True,choices=ROOM_CATEGORIES)
    hotel = models.ForeignKey(Hotel,on_delete=models.CASCADE)
    is_refundable = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'{self.number}. {self.category} for {self.capacity} people'
    

class AirPort(models.Model):
    class Meta:
        db_table = 'AirPort'
    name = models.CharField(max_length=200)
    city = models.ForeignKey(City,on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self) -> str:
        return f'{self.name}'
    
class Flight(models.Model):
    class Meta:
        db_table = 'Flight'
    name = models.CharField(max_length=100,null=True,unique=True,validators=[
        RegexValidator(
            regex=r'^FLY\w+',
            message='Flight name must start with "FLY"'
        )
    ])    
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField(null=True, blank=True)
    price = models.DecimalField(max_digits=6,decimal_places=2)
    is_Refundable = models.BooleanField()
    image = models.URLField()
    airport_from = models.ForeignKey(AirPort,on_delete=models.CASCADE ,related_name="departure")    
    airport_to = models.ForeignKey(AirPort,on_delete=models.CASCADE ,related_name="arrival")

    def clean(self):
        if self.departure_time < timezone.now():
            raise ValidationError('Departure time must be in the future')
        
        if self.departure_time > self.arrival_time:
            raise ValidationError('Arrival time must be after departure time')
        
    def duration(self):
        if self.departure_time and self.arrival_time:
            return self.arrival_time - self.departure_time
        else:
            return timedelta()   

    def __str__(self) -> str:
        return f'{self.airport_from} to {self.airport_to} on {self.departure_time.strftime("%d/%m/%Y")}'

class flightAvailableSeats(models.Model):
    class Meta:
        db_table = 'flight_available_seats'
        unique_together = [('flight','airplane')]
    available_seats = models.IntegerField(null=True,blank=True)
    flight = models.ForeignKey(Flight,on_delete=models.CASCADE)
    airplane = models.ForeignKey(Airplane,on_delete=models.CASCADE)

    def save(self,args,*kwargs):
        if not self.available_seats:
            self.available_seats = self.airplane.type.capacity if self.airplane.type else None
        super().save(args,*kwargs)    

    def __str__(self) -> str:
        return f'{self.flight.__str__()} in {self.airplane} with {self.available_seats} available'
    
    def decrement_available_seats(self):
        if self.available_seats is not None:
            self.available_seats -= 1
            self.save()
    
    def decrement_available_seats(self):
        if self.available_seats is not None:
            self.available_seats -= 1
            self.save()



class Booking(models.Model):
    class Meta:
        db_table = 'Booking'
    date = models.DateField() 
    cost = models.DecimalField(decimal_places=2,max_digits=6)  #lezim zabeta hay champ calcule
    cancel_date = models.DateField(null=True)
    payment_date = models.DateField()
    flight = models.ForeignKey(Flight,on_delete=models.CASCADE,default=None)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    is_refunded = models.BooleanField(null=True, blank=True)
    
    def _str_(self) -> str:
        return f'{self.flight._str_()} in {self.user}'
    
    @property
    def status(self):#hayde yeene metl function lal class kermel ne3mol control aal field li eena yehon 
        current_date = timezone.now().date() #year-month-day
        

        if current_date < self.flight.departure_time.date():
            return 'Upcoming'
        elif self.flight.departure_time.date() <= current_date <= self.flight.arrival_time.date():
            return 'Ongoing'
        elif current_date > self.flight.arrival_time.date():
            return 'Completed'
        else:
            return 'Unknown'   
 

class RoomBooked(models.Model):
    class Meta:
        db_table = 'RoomBooking'      
    room = models.ForeignKey(Room,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    checkin = models.DateTimeField()
    checkout = models.DateTimeField()
    payment_date = models.DateField()
    cancel_date = models.DateTimeField(null=True)
    cost=models.DecimalField(decimal_places=2,max_digits=6,default=1000)
    is_refunded = models.BooleanField(null=True, blank=True)

    @property
    def status(self):#hayde yeene metl function lal class kermel ne3mol control aal field li eena yehon 
        current_date = timezone.now().date() #year-month-day
        

        if current_date < self.checkin.date():
            return 'Upcoming'
        elif self.checkin.date() <= current_date <= self.checkout.date():
            return 'Ongoing'
        elif current_date > self.checkout.date():
            return 'Completed'
        else:
            return 'Unknown'







    
from django.contrib import admin
from .models import User ,Hotel,Room,City,Country,Flight,Booking,RoomBooked,Airline,AirPort,Payment,flightAvailableSeats,Airplane,Airplane_type
# Register your models here.
admin.site.register(User)
admin.site.register(Hotel)
admin.site.register(Room)
admin.site.register(Booking)
admin.site.register(RoomBooked)
admin.site.register(Flight)
admin.site.register(Airline)
admin.site.register(Payment)
admin.site.register(City)
admin.site.register(AirPort)
admin.site.register(Country)
admin.site.register(flightAvailableSeats)
admin.site.register(Airplane)
admin.site.register(Airplane_type)

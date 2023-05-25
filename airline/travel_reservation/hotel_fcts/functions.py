import datetime
from travel_reservation.models import Room,RoomBooked,Booking

def check_availability(room,check_in,check_out):
    avail_list=[]
    Booking_list=RoomBooked.objects.filter(room=room)
    for booking in Booking_list:
        if booking.checkin>check_out or booking.checkout<check_in:
            avail_list.append(True)
        else:
            avail_list.append(False)    
    return all(avail_list)          #all yaane betred true eza kel l elements yali bel list hene True
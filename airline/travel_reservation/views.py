from datetime import datetime
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm # Built in class form to create a user
from .forms import CreateUserForm
from .models import Flight,Booking,RoomBooked,Room,flightAvailableSeats,Hotel,City
from django.contrib.auth.views import LoginView
from .models import Flight,flightAvailableSeats,Booking,Hotel,Room,RoomBooked
from .forms import AuthenticateUserForm,flightForm
from django.utils import timezone
from django.core.mail import EmailMessage
from django.db.models import Q
from django.conf import settings
from django.template.loader import render_to_string
import pdfkit
from decimal import Decimal

from .forms import AuthenticateUserForm
from datetime import datetime
import time 
from django.utils import timezone
# table user built in

# Create your views here.
def home_view(request):
    hotels=Hotel.objects.all()
    cities=City.objects.all()
    return render(request,'home.html',{'nav':"home",'hotels':hotels,'cities':cities})\
    
def room_list_view(request, hotel_id):
    hotel = Hotel.objects.get(pk=hotel_id)
    rooms = Room.objects.filter(hotel=hotel)
    return render(request, 'room_list.html', {'hotel': hotel, 'rooms': rooms})    

def signup_view(request):
    
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()
            
            return redirect('/Login/')

    else:
        form = CreateUserForm() 

    return render(request,'authentication/signup.html',{
        'form' : form
    })

def flight_view(request):

    form = flightForm()
    
   # if request.method == 'GET':
    #    form = flightForm(request.GET)
    context = {
        'form' : form,
        'nav' : 'flight'
    }

    return render(request,'flight.html',context)

def search_results_view(request):
     
    city1 = request.GET.get('airport_from')
    city2 = request.GET.get('airport_to')
    departure_date = request.GET.get('departure_time')


    returning_flight = request.GET.get('Departure_time_2')
    
    # flights = Flight.objects.filter(
    #    airport_from__city = city1,
    #    airport_to__city = city2,
    #    departure_time__gte=departure_date
    # )

    flights = flightAvailableSeats.objects.filter(flight__airport_from__city = city1, flight__airport_to__city = city2,flight__departure_time__gte=departure_date,available_seats__gt = 0)
    
    if returning_flight != "":
        flights_returning = Flight.objects.filter(
            airport_from__city = city2,
            airport_to__city = city1,
            departure_time__gte=returning_flight
        )
       

    context = {
        'flights' : flights,
        'flightsReturning': flights_returning if returning_flight else None
    }
    return render(request,'search_results.html',context)        

def flight_Details(request):

    flightID = request.GET.get('flightId')
    f = flightAvailableSeats.objects.get(id=flightID)
    context = {
        'f' : f
    }
    
    return render(request,'flight_booking.html',context)


def payment_flight(request):
    flightID = request.GET.get('flightId')
    f = Flight.objects.get(id=flightID)

    if request.method == 'POST':
        template = render_to_string('email_template.html', {'name': "Charbel"})
        pdf_options = {
            'quiet': '',
            'page-size': 'Letter',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
        }
        path_to_wkhtmltopdf = 'C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe'
        pdf = pdfkit.from_string(template, False,  configuration=pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf),options=pdf_options)

        Booking.objects.create(date=timezone.now().date(), cost=f.price, flight=f, user=request.user, payment_date=timezone.now().date())
        flightAvSeats = flightAvailableSeats.objects.get(flight=f)
        flightAvSeats.decrement_available_seats()

        email = EmailMessage(
            'Thanks for booking a flight',
            template,
            settings.EMAIL_HOST_USER,
            ['vanessakhourieh@gmail.com']
        )
        email.content_subtype = "html"
        email.fail_silently = False
        email.attach('file.pdf', pdf, 'application/pdf')
        email.send()
        return HttpResponseRedirect("/", status=303)

    response = render(request, 'payment.html', {'price': f.price})
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

def hotel_view(request):   
     hotels = Hotel.objects.none()  
     if request.method == 'GET':    #bss yektoub a word bel search ,he will search for any hotel having name=word aw city=word aw country=word
        query=request.GET.get('query')
        if query:
            hotels = Hotel.objects.filter(Q(name__icontains=query) | Q(city__name__icontains=query) | Q(city__country__name__icontains=query))
     context = {'hotels': hotels ,'nav': "hotel"}


     return render(request, 'hotel.html', context)   


def rooms_detail_view(request): #when clicking on an item of the hotels results he will be redirected for the room detail of this hotel
    if request.method=='POST':
        
        check_in_date = request.POST.get('check-in-date')
        check_out_date = request.POST.get('check-out-date')
        check_in_time = request.POST.get('check-in-time')
        check_out_time = request.POST.get('check-out-time')
        hotelId=request.POST.get('hotelId')
        hotel=int(hotelId)#hawalna l str la int
        NbPers=request.POST.get('pers')
        if NbPers:
          NbPers=int(NbPers)
        
        RoomType=request.POST.get('roomType')
        
        
        check_in_date1 = datetime.strptime(check_in_date, '%Y-%m-%d').date()  #converting l inputet men str la date and time objects la2n hatta
        #law type tabaoun hue date bel model hone i will get them as string
        check_out_date1 = datetime.strptime(check_out_date, '%Y-%m-%d').date()
        check_in_time1 = datetime.strptime(check_in_time, "%H:%M").time()
        check_out_time1 = datetime.strptime(check_out_time, "%H:%M").time()
        

        if check_in_date1 >= check_out_date1 or check_in_date1 < datetime.now().date():
            errorDate="Make sure the dates are correct!"
            Hotels=Hotel.objects.get(id=hotelId)
            context1={'errorDate':errorDate,'hotel':Hotels}
            return render(request,'roomBooking_details.html',context1)
            


        check_in_datetime = datetime.combine(check_in_date1, check_in_time1)
        check_out_datetime = datetime.combine(check_out_date1, check_out_time1)

        booked_rooms = RoomBooked.objects.filter(
        Q(checkin__range=(check_in_datetime, check_out_datetime)) | #check if check in tabaa l room booked falls bi hal range 
        Q(checkout__range=(check_in_datetime, check_out_datetime)) |#check if l check out tabaa l room booked falls bi hal range
        Q(checkin__lte=check_in_datetime, checkout__gte=check_out_datetime) #checks eza l range yali mfawata l user mawjoude kela bi range l room booked
           ).values_list('room_id', flat=True) #betred flat list containing l room id tabaa l rooms that checks one of these conditions
    
        #Get the available rooms by excluding the booked rooms
        results=Room.objects.filter(hotel_id=hotelId) #capacity__gte=nbPers yaane betredele l capacity yali greater or equal la yali mfawata l user
        if RoomType:
         results = results.filter(category=RoomType)
        if NbPers:
         results = results.filter(capacity__gte=NbPers) 
        
        available_rooms = results.exclude(id__in=booked_rooms)

       
        
        context={'rooms':available_rooms,'check_in_date': check_in_date1,'check_out_date':check_out_date1,
                 'check_in_time':check_in_time1,'check_out_time':check_out_time1 }
        return render(request,'rooms_details.html',context)
    
    return render(request, 'roomBooking_details.html')

def checkRoom_availability_view(request,hotel_id):
     Hotels=Hotel.objects.get(id=hotel_id)
     context={'hotel':Hotels}
    
     return render(request,'roomBooking_details.html',context)

def hotel_Room_payment_view(request):  #when clicking on 'Book now of a room 'it will direct us to the payment view
     if request.method=='POST':
         room_Id=request.POST.get('room_id')
         check_in=request.POST.get('check_in_date')
         check_out=request.POST.get('check_out_date')
         in_time=request.POST.get('check_in_time')
         out_time=request.POST.get('check_out_time')
         print(in_time)
         print("hellooooooooooooooooooooooooooo")
    
         room=Room.objects.get(id=room_Id)
         context={'room':room,'check_in':check_in,'check_out':check_out,'in_time':in_time,'out_time':out_time}
         return render(request,'hotelRoomPayment.html',context)

def payment_process_view(request): #when we submit l payment
    if request.method=='POST':
        check_in=request.POST.get('check_in_date')
        check_out=request.POST.get('check_out_date')
        in_time=request.POST.get('check_in_time')
        out_time=request.POST.get('check_out_time')
        room_id=request.POST.get('room_id')
        room_Id=int(room_id)
        cost=request.POST.get('room_Cost')
        cost=Decimal(cost)
        
        print(in_time)
        print("hellooooooooooooooooo")
        check_in = datetime.strptime(check_in, '%B %d, %Y').date()
        check_out = datetime.strptime(check_out, '%B %d, %Y').date()
        in_time = datetime.strptime(in_time  , "%H:%M").time()
        out_time = datetime.strptime(out_time ,  "%H:%M").time()

        check_in_datetime = datetime.combine(check_in, in_time)
        check_out_datetime = datetime.combine(check_out, out_time)
        room_booked = RoomBooked.objects.create(
            checkin=check_in_datetime,
            checkout=check_out_datetime,
            payment_date=timezone.now(),
            user_id=request.user.id,  # Assuming you have a logged-in user
            room_id=room_Id,
            cost=cost
         )
        

        message="Payment successfull!"
        context={'message':message}
        return render(request,'hotelRoomPayment.html',context)

def profile_view(request): 
  resultsBooking=Booking.objects.filter(user=request.user)

 
  


  print(resultsBooking)
  numberOfFlightBookings=len(resultsBooking)


  resultsRoomBooked=RoomBooked.objects.filter(user=request.user)
  #booking__user (hayde kent hattayta bl filter bas rj3na zabatna) bas ma st3mlnha laeno rj3na zabatna bas tarakta kermel l rmq
  # b aleb l model roomBooked eena fk esmo booking , w ta ousal lal field user tb3 l class booking
  #  be3mol hal tari2a


  
  current_date = datetime.now().date()
  formatted_date = current_date.strftime('%Y-%m-%d')
  #%B represents the full month name (e.g., "MAY").
#%d represents the day of the month as a zero-padded decimal number (e.g., "25").
#%Y represents the year with a century as a decimal number (e.g., "2023").
#%I represents the hour (12-hour clock) as a zero-padded decimal number (e.g., "07").
#%M represents the minute as a zero-padded decimal number (e.g., "10").
#%p represents either "AM" or "PM" based on the given time (e.g., "P.M.").

  

  



  
  return render(request,'profile.html',{'nav':"profile",'resultsBooking':resultsBooking,'numberOfBookings':numberOfFlightBookings,'roomBooked':resultsRoomBooked,'current_time':formatted_date})




def cancel_room_view(request,roombooked_id=0):


    resultsBooking=Booking.objects.filter(user=request.user)
    numberOfFlightBookings=len(resultsBooking)


    resultsRoomBooked=RoomBooked.objects.filter(user=request.user)

   
    current_date = datetime.now().date()
    formatted_date = current_date.strftime('%Y-%m-%d')
   
    if roombooked_id !=0:
     roombooked=RoomBooked.objects.get(id=roombooked_id)
     roombooked.cancel_date=formatted_date
     roombooked.is_refunded=True
     roombooked.save()

    return render(request,'profile.html',{'nav':"profile",'resultsBooking':resultsBooking,'numberOfBookings':numberOfFlightBookings,'roomBooked':resultsRoomBooked,'current_time':formatted_date})



def cancel_flight_view(request,flight_id):
   # 3tine defalut value lal flight_id kermel awal mara mn 3ayit he l view ma b koun fi flight_id 
   # hayde l flight_id rah n2ate3a bl click aal btn cancel bl profile.html
    #se3eta khls bl profile.html kermel e3mol control aal dates (dep w arrival bas be3mol booking.status)

   resultsBooking=Booking.objects.filter(user=request.user)
   numberOfFlightBookings=len(resultsBooking)

   resultsRoomBooked=RoomBooked.objects.filter(user=request.user)

   current_date = datetime.now().date()
   formatted_date = current_date.strftime('%Y-%m-%d')
  #%B represents the full month name (e.g., "MAY").
#%d represents the day of the month as a zero-padded decimal number (e.g., "25").
#%Y represents the year with a century as a decimal number (e.g., "2023").
#%I represents the hour (12-hour clock) as a zero-padded decimal number (e.g., "07").
#%M represents the minute as a zero-padded decimal number (e.g., "10").
#%p represents either "AM" or "PM" based on the given time (e.g., "P.M.").

   if flight_id !=0:  # to cancel a flight (modify the cancel date in the database )
    flight = Flight.objects.get(id=flight_id)
    temp=Booking.objects.get(flight=flight)
    temp.cancel_date=formatted_date
    if temp.flight.is_Refundable == True:
        temp.is_refunded=True
       
   # ide aal rab saad batal 
    temp2=flightAvailableSeats.objects.get(flight=flight)
    print(temp2.available_seats)
    temp2.available_seats=temp2.available_seats+1
    print(temp2.available_seats)


    
    temp.save()

    print(flight)

   return render(request,'profile.html',{'nav':"profile",'resultsBooking':resultsBooking,'numberOfBookings':numberOfFlightBookings,'roomBooked':resultsRoomBooked,'current_time':formatted_date})
   
#Login View is built in
class login_view(LoginView):
   
   form_class = AuthenticateUserForm
   template_name = 'authentication/login.html'

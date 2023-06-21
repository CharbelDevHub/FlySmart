from datetime import datetime
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm # Built in class form to create a user
from .forms import CreateUserForm
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

# table user built in

# Create your views here.
def home_view(request):
    return render(request,'home.html',{'nav':"home"})

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
    return render(request,'profile.html')
#Login View is built in

class login_view(LoginView):
   
   form_class = AuthenticateUserForm
   template_name = 'authentication/login.html'

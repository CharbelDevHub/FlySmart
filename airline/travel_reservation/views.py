from datetime import datetime
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm # Built in class form to create a user
from .forms import CreateUserForm
from django.contrib.auth.views import LoginView
from .models import Flight,flightAvailableSeats,Booking
from .forms import AuthenticateUserForm,flightForm
from django.utils import timezone
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
import pdfkit

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

    return render(request,'hotel.html',{'nav':"hotel"})

#Login View is built in

class login_view(LoginView):
   
   form_class = AuthenticateUserForm
   template_name = 'authentication/login.html'

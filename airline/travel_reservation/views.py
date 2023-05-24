from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm # Built in class form to create a user
from .forms import CreateUserForm
from django.contrib.auth.views import LoginView
from .models import Flight
from .forms import AuthenticateUserForm,flightForm
# table user built in

# Create your views here.
def home_view(request):
    return render(request,'home.html',{'nav':"home"})

def signup_view(request):
    
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect('/Login/')

    else:
        form = CreateUserForm() 

    return render(request,'authentication/signup.html',{
        'form' : form
    })

def flight_view(request):
    form = flightForm()
    
    if request.method == 'GET':
        form = flightForm(request.GET)
       

    context = {
        'form' : form,
        'nav' : 'flight'
    }
    return render(request,'flight.html',context)

def search_results_view(request):
     
    airport1 = request.GET.get('airport_from')
    airport2 = request.GET.get('airport_to')
    departure_date = request.GET.get('departure_time')
    arrival_date = request.GET.get('arrival_time')
    
    flights = Flight.objects.filter(
       airport_from = airport1,
       airport_to = airport2,
       departure_time__gte=departure_date,
       arrival_time__lte = arrival_date 
    )
    context = {
        'flights' : flights
    }
    return render(request,'search_results.html',context)        

def hotel_view(request):

    return render(request,'hotel.html',{'nav':"hotel"})

#Login View is built in

class login_view(LoginView):
   
   form_class = AuthenticateUserForm
   template_name = 'authentication/login.html'

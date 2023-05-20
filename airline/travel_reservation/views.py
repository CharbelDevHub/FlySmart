from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm # Built in class form to create a user
from .forms import CreateUserForm
from django.contrib.auth.views import LoginView
from .forms import AuthenticateUserForm
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
    return render(request,'flight.html',{'nav': "flight" })

def hotel_view(request):
    return render(request,'hotel.html',{'nav':"hotel"})

#Login View is built in

class login_view(LoginView):
   
   form_class = AuthenticateUserForm
   template_name = 'authentication/login.html'

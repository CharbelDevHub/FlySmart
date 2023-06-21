from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from travel_reservation.models import User,Flight,AirPort,City


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2','first_name','last_name','birthdate']

    username = forms.CharField(widget=forms.TextInput(attrs={
        'type' : 'name',
        'id' : 'username',
        'class' : 'form-control border-0 border-bottom',
        "placeholder" : "Username"
    }))    # Adding attributes to the tag <input>

    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'type' : 'email',
        'id' : 'email',
        'class' : 'form-control border-0 border-bottom',
        'placeholder' : 'Email:'
    }))

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'type' : 'password',
        'id' : 'password1',
        'class' : 'form-control border-0 border-bottom',
        'placeholder': 'Enter your password'
    }))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'type' : 'password',
        'id' : 'password2',
        'class' : 'form-control border-0 border-bottom',
        'placeholder': 'Enter your password'
    }))

    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'type' : 'name',
        'id' : 'firstname',
        'class' : 'form-control border-0 border-bottom',
        'placeholder': 'FirstName'
    }))

    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'type' : 'name',
        'id' : 'lastname',
        'class' : 'form-control border-0 border-bottom',
        'placeholder': 'LastName'
    }))

    birthdate = forms.DateField(widget=forms.DateInput(attrs={
        'type' : 'date',
        'id' : 'birthdate',
        'class' : 'form-control',
        'placeholder' : 'birthdate'
    }))

class AuthenticateUserForm(AuthenticationForm):
    
    error_messages = {
        'invalid_login': 'Your username and/or password is incorrect. Please try again.',
        'inactive': 'This account is inactive.',
    }

    username = forms.CharField(widget=forms.TextInput(attrs={
        'type' : 'name',
        'id' : 'username',
        'class' : 'form-control border-0 border-bottom',
        "placeholder" : "Username"
    }))       

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'type' : 'password',
        'id' : 'password1',
        'class' : 'form-control border-0 border-bottom',
        'placeholder': 'Enter your password'
    }))    


class flightForm(forms.ModelForm):
    class Meta:
        model = Flight
        fields = ['airport_from','airport_to','departure_time','arrival_time']
    

    airport_from = forms.ModelChoiceField(queryset=City.objects.all() ,widget=forms.Select(attrs={
        'id' : 'airport1',
        'class' : 'form-select'
    }))

    airport_to = forms.ModelChoiceField(queryset=City.objects.all() ,widget=forms.Select(attrs={
        'id' : 'airport2',
        'class' : 'form-select'
    }))

    departure_time = forms.DateField(widget=forms.DateInput(attrs={
        'id' : 'departure',
        'type' : 'date',
        'class' : 'form-control'
    }
    ))

    is_RoundTrip = forms.BooleanField(required=False,widget=forms.CheckboxInput(attrs={
        'id' : 'roundtrip',
        'class' : 'form-check-input '
    }))


    
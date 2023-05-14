from django.urls import path
from .views import home_view,signup_view,login_view

urlpatterns = [
    path('',home_view),
    path('Signup/',signup_view),
    path('Login/',login_view.as_view()) #specifying the location of the html file
    
]

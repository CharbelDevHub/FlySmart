from django.urls import path
from .views import home_view,signup_view,login_view,profile_view,cancel_flight_view,room_list_view,cancel_room_view,flight_view,hotel_view,search_results_view,flight_Details,payment_flight,rooms_detail_view,hotel_Room_payment_view,payment_process_view,checkRoom_availability_view

urlpatterns = [
    path('',home_view),
    path('Signup/',signup_view),
    path('Login/',login_view.as_view()),#specifying the location of the html file
    path('Flight/',flight_view,name="flight"),
    path('Hotel/',hotel_view,name="hotel"),
    path('search/',search_results_view,name='search_results'),
    path('FlightDetails/',flight_Details,name='flight_Booking'),
    path('Flight/payment',payment_flight,name='flight_payment'),
    path('Rooms/',rooms_detail_view, name='rooms_detail_view'),
    path('RoomBooking/<int:hotel_id>/',checkRoom_availability_view, name='room_availability'),
    path('RoomPayment/',hotel_Room_payment_view,name='hotelRoomPay'), #l name yali aam hoto hue l l url yali bel ahref hattino lal button
    path('PaymentSuccessfull/',payment_process_view,name='paymentProcess'),
    path('Profile/',profile_view,name="profile"),
    path('cancel/<int:flight_id> /', cancel_flight_view, name='cancelF'),  #cancelF for cancel Flight  (this name will be used in the form in the html )
    path('cancel/room/<int:roombooked_id>/',cancel_room_view,name="cancelR"), #cancelR for cancel room (this name will be used in the form in profile.html)
    path('rooms/<int:hotel_id>/',room_list_view, name='room_list')
    
]

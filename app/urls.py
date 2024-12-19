from django.contrib import admin
from django.urls import path
from . import views 
from .views import Home,VoiceResponseView,VolunteerView

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('vol/', VolunteerView.as_view(), name='vol'),
    path('submit-details/', Home.as_view(), name='submit_details'),  
    path('sos/', views.SosPageView.as_view(), name='sos_page'),
    path('send-sos/', views.SosView.as_view(), name='sos'),  
    path('gdacs-map/', views.GDACSMapView.as_view(), name='gdacs_map'),  
    path('voice-response/', VoiceResponseView.as_view(), name='voice_response'),


]
    

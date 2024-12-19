from django.shortcuts import render, HttpResponse
from django.views import View
from .models import User
from twilio.rest import Client  
import requests
from django.conf import settings
import xml.etree.ElementTree as ET
from twilio.twiml.voice_response import VoiceResponse


class Home(View):
    def get(self, request):
        name = request.COOKIES.get('name', '')
        phone = request.COOKIES.get('phone', '')
        address = request.COOKIES.get('address', '')
        return render(request, 'home.html', {'name': name, 'phone': phone, 'address': address})

    def post(self, request):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address = request.POST.get('address')
        pin_code = request.POST.get('pin_code')

        try:
            user = User.objects.create(
                name=name,
                phone=phone,
                email=email,
                address=address,
                pin_code=pin_code
            )
        

            self.send_call(phone, name)

            response = HttpResponse("Details submitted successfully!")

            response.set_cookie('name', name, max_age=365 * 24 * 60 * 60)  
            response.set_cookie('phone', phone, max_age=365 * 24 * 60 * 60)  
            response.set_cookie('address', address, max_age=365 * 24 * 60 * 60)  

            return response
        except Exception as e:
            return HttpResponse(f"An error occurred: {e}")

    def send_call(self, phone, name):
        account_sid = 'AC81abb4fa7b14b37c53ae46719b9d699c'  # Twilio Account SID
        auth_token = '2c9c321317d7678675f3cb577cfbd8d4'  # Twilio Auth Token
        from_number = '+12295151239'  # Your Twilio phone number

        client = Client(account_sid, auth_token)

        # You need a URL that returns TwiML (XML) to tell Twilio how to handle the call
        twiml_url = 'http://your-server.com/voice-response'  # Replace with your URL

        # Make a voice call
        call = client.calls.create(
            to=phone,
            from_=from_number,
            url=twiml_url  # This URL will handle what Twilio says during the call
        )

        print(f"Call initiated to {phone}: {call.sid}")

class VoiceResponseView(View):
    def get(self, request):
        # Create a Twilio response that says a message when the call is answered
        response = VoiceResponse()
        response.say(f"Hello {request.GET.get('name')}, your details have been successfully submitted. Thank you!", voice='alice')

        return HttpResponse(str(response), content_type='application/xml')
class SosPageView(View):
    def get(self, request):
        return render(request, 'sos.html')

class SosView(View):
    def post(self, request):
        name = request.COOKIES.get('name', '')
        phone = request.COOKIES.get('phone', '')
        address = request.COOKIES.get('address', '')

        if phone:
            phone = '+91' + phone[-10:]  # Formatting the phone number to include the country code

        sos_phone_number = '+91' + '9686635137'  # The fixed SOS recipient number

        # Prepare the custom message for the SMS and the voice call
        message_body = f"User {name} is in trouble! Phone: {phone}. Address: {address}"

        try:
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

            # Send SMS to the recipient
            client.messages.create(
                body=message_body,
                from_=settings.TWILIO_PHONE_NUMBER,
                to=sos_phone_number
            )

            # Prepare the TwiML URL (replace with your actual server endpoint)
            try:
                custom_message = f"Attention! A person {name} is in trouble ! "

                call = client.calls.create(
                    twiml=f'<Response><Say>{custom_message}</Say></Response>',
                    from_=settings.TWILIO_PHONE_NUMBER,  # Your Twilio phone number
                    to="+919686635137"  # The user's phone number
                )
                print(f"Call initiated to : {call.sid}")
            except Exception as e:
                print(f"Error making call to : {e}")

            return HttpResponse("SOS call and SMS initiated successfully!")
        except Exception as e:
            return HttpResponse(f"An error occurred while sending the SOS call and SMS: {e}")
        
        
        
class GDACSMapView(View):
    def get(self, request):
        try:
            response = requests.get('https://www.gdacs.org/xml/rss.xml')
            response.raise_for_status()  # Raise an exception for bad responses
            
            # Log the response text to check the actual content
            print(response.text)  # Debug: check the raw response data

            xml_data = response.text  # Get the raw XML data from GDACS

            # Parse the XML data to extract relevant info
            root = ET.fromstring(xml_data)
            disasters = []
            for item in root.findall('.//item'):
                title = item.find('title').text
                description = item.find('description').text
                coordinates = item.find('geo:lat').text if item.find('geo:lat') is not None else None
                longitude = item.find('geo:long').text if item.find('geo:long') is not None else None
                if coordinates and longitude:
                    disasters.append({
                        'title': title,
                        'description': description,
                        'latitude': coordinates,
                        'longitude': longitude,
                    })

            return render(request, 'gdacs_map.html', {'disasters': disasters})
        except requests.RequestException as e:
            return render(request, 'gdacs_map.html', {'error': f'Error fetching GDACS data: {e}'})
        except ET.ParseError as e:
            return render(request, 'gdacs_map.html', {'error': f'Error parsing XML: {e}'})


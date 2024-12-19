from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Disaster, User, Volunteer
from twilio.rest import Client
from django.conf import settings

@receiver(post_save, sender=Disaster)
def make_call_on_disaster_creation(sender, instance, created, **kwargs):
    if created:
        # Query Users and Volunteers in the same pin code area separately
        users_in_disaster_area = User.objects.filter(pin_code=instance.pin_code)
        
        # Treat pin_code as a string and manipulate it accordingly
        pin_code_str = str(instance.pin_code)
        surrounding_pins = [
            pin_code_str,  # Same pin code
            str(int(pin_code_str) + 1),  # Next pin code
            str(int(pin_code_str) + 2),  # Two pin codes away
            str(int(pin_code_str) - 1),  # Previous pin code
            str(int(pin_code_str) - 2)   # Two pin codes away back
        ]

        volunteers_in_disaster_area = Volunteer.objects.filter(pin_code__in=surrounding_pins)

        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

        # Send calls to Users
        for user in users_in_disaster_area:
            try:
                custom_message = f"Attention! A new disaster named {instance.name} has occurred in your area. {instance.description}"

                call = client.calls.create(
                    twiml=f'<Response><Say>{custom_message}</Say></Response>',
                    from_=settings.TWILIO_PHONE_NUMBER,  # Your Twilio phone number
                    to=user.phone  # The user's phone number
                )
                print(f"Call initiated to User {user.phone}: {call.sid}")
            except Exception as e:
                print(f"Error making call to User {user.phone}: {e}")

        # Send calls to Volunteers
        for volunteer in volunteers_in_disaster_area:
            try:
                custom_message = f"Attention! A new disaster named {instance.name} has occurred in your area. {instance.description}"

                call = client.calls.create(
                    twiml=f'<Response><Say>{custom_message}</Say></Response>',
                    from_=settings.TWILIO_PHONE_NUMBER,  
                    to=volunteer.phone  
                )
                print(f"Call initiated to Volunteer {volunteer.phone}: {call.sid}")
            except Exception as e:
                print(f"Error making call to Volunteer {volunteer.phone}: {e}")

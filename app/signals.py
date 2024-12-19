from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Disaster, User
from twilio.rest import Client
from django.conf import settings

@receiver(post_save, sender=Disaster)
def make_call_on_disaster_creation(sender, instance, created, **kwargs):
    if created:
        users_in_disaster_area = User.objects.filter(pin_code=instance.pin_code)

        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

        for user in users_in_disaster_area:
            try:
                custom_message = f"Attention! A new disaster named {instance.name} has occurred in your area. {instance.description}"

                call = client.calls.create(
                    twiml=f'<Response><Say>{custom_message}</Say></Response>',
                    from_=settings.TWILIO_PHONE_NUMBER,  # Your Twilio phone number
                    to=user.phone  # The user's phone number
                )
                print(f"Call initiated to {user.phone}: {call.sid}")
            except Exception as e:
                print(f"Error making call to {user.phone}: {e}")

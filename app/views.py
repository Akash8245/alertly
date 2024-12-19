from django.shortcuts import render, HttpResponse
from django.views import View
from .models import User 

class Home(View):
    def get(self, request):
        name = request.COOKIES.get('name', '')
        phone = request.COOKIES.get('phone', '')
        return render(request, 'home.html', {'name': name, 'phone': phone})

    def post(self, request):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address = request.POST.get('address')
        pin_code = request.POST.get('pin_code')

        try:
            User.objects.create(
                name=name,
                phone=phone,
                email=email,
                address=address,
                pin_code=pin_code
            )
            response = HttpResponse("Details submitted successfully!")
            response.set_cookie('name', name, max_age=365 * 24 * 60 * 60)  
            response.set_cookie('phone', phone, max_age=365 * 24 * 60 * 60)  
            response.set_cookie('address', phone, max_age=365 * 24 * 60 * 60)  

            return response
        except Exception as e:
            return HttpResponse(f"An error occurred: {e}")

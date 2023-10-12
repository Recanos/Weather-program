import requests
from django.shortcuts import render
from .models import City
from .forms import CityForm

# Create your views here.
def index(request):
    API_key = '795e457b87c6d307d19165ae3f930411'
    url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid=" + API_key + '&units=metric'
    
    if request.method=="POST":
        form_p = CityForm(request.POST)
        form_p.save()
    
    form_p = CityForm()

    cities = City.objects.all()
    all_cities = []
    for city in cities:

        res = requests.get(url.format(city.name)).json()


        city_info = {
            'city' : city.name,
            'temp' : res['main']['temp'],
            "icon" : res['weather'][0]['icon'],
            'wind' : res['wind']['speed'],

        }
        
        all_cities.append(city_info)

    context = {'all_form' : all_cities, 'form' : form_p}
    return render(request, 'weather/index.html', context)
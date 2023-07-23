# weather/views.py

from django.shortcuts import render, redirect
import requests
from .models import City
from .forms import CityForm
from .models import UserPreferences
from django.contrib.auth.forms import UserCreationForm
from .models import UserPreferences
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=1effb1a3c2a8e3e7d4d048beb79765b4'

    cities = City.objects.all() #return all the cities in the database
    
    if request.method == 'POST': # only true if form is submitted
        form = CityForm(request.POST) # add actual request data to form for processing
        form.save() # will validate and save if validate

    form = CityForm()
    
    weather_data = []

    for city in cities:

        city_weather = requests.get(url.format(city)).json() #request the API data and convert the JSON to Python data types

        weather = {
            'city' : city,
            'temperature' : city_weather['main']['temp'],
            'description' : city_weather['weather'][0]['description'],
            'icon' : city_weather['weather'][0]['icon']
        }

        weather_data.append(weather) #add the data for the current city into our list

    context = {'weather_data' : weather_data, 'form' : form}

    return render(request, 'weather/index.html', context) #returns the index.html template


def weather_detail(request, city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=imperial&appid=1effb1a3c2a8e3e7d4d048beb79765b4'

    city_weather = requests.get(url).json()

    context = {
        'city': city,
        'temperature': city_weather['main']['temp'],
        'description': city_weather['weather'][0]['description'],
        'humidity': city_weather['main']['humidity'],
        'wind_speed': city_weather['wind']['speed'],
        'visibility': city_weather['visibility'],
        'icon': city_weather['weather'][0]['icon']
    }

    return render(request, 'weather/weather_detail.html', context)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserPreferences.objects.create(user=user)  # Create user preferences object
            return redirect('index')  # Redirect to the home page after registration
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})


@login_required
def save_city(request):
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            city_name = form.cleaned_data['name']
            user = request.user
            city = City(name=city_name, user=user)
            city.save()
            return redirect('user_city')  
    else:
        form = CityForm()
    return render(request, 'weather/save_city.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('index')

def user_city(request):
    if request.user.is_authenticated:
        user_saved_cities = City.objects.filter(user=request.user)
        return render(request, 'weather/user_city.html', {'user_saved_cities': user_saved_cities})
    else:
        return redirect('login')
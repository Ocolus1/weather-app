from django.shortcuts import render, redirect
import requests
from .models import City
from .forms import CityForm

# Create your views here.
def index(request):
    url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=dd8e9b4ce477a0ad8b1a26022cfdc1b3"

    if request.method == "POST":
        form = CityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")

    form = CityForm()

    weather_data = []

    cities = City.objects.all()

    for city in cities:
        r = requests.get(url.format(city)).json()

        city_weather = {
            "id": city.id,
            "city" : city.name,
            "temperature": r["main"]["temp"],
            "description": r["weather"][0]["description"],
            "icon": r["weather"][0]["icon"],
        }

        weather_data.append(city_weather)

    context = {"weather_data": weather_data, "form": form}
    return render(request, "weather/index.html", context)


def delete_city(request, id):
    city = City.objects.get(pk=id)

    
    city.delete()

    return redirect("/")
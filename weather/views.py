from django.shortcuts import render, redirect
import requests

# Create your views here.

def index(request):
    url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid={}"
    app_id = "dd8e9b4ce477a0ad8b1a26022cfdc1b3"
    if "cities" not in request.session:
        request.session["cities"] = []
    
    if request.method == "POST":
        city = request.POST["city"]
        saved_list = request.session['cities']
        saved_list.append(city)
        request.session['cities'] = saved_list
        return redirect("/")
    
    weather_data = []

    for city in request.session["cities"]:
        r = requests.get(url.format(city,app_id)).json()
        if r['cod'] == "404":
            city_weather = {
                "city" : f"{city} does not exist",
                "temperature": None,
                "description": None,
                "icon": None,
            }
        else: 
            city_weather = {
                "city" : city,
                "temperature": r["main"]["temp"],
                "description": r["weather"][0]["description"],
                "icon": r["weather"][0]["icon"],
            }

        weather_data.append(city_weather)

    weather_data.reverse()
    context = {"weather_data": weather_data }
    return render(request, "weather/index.html", context)


def delete_city(request, city):
    saved_list = request.session['cities']
    saved_list.remove(city)
    request.session['cities'] = saved_list
    return redirect("/")

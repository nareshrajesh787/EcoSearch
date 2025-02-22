from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from geopy.geocoders import Nominatim

from .forms import homeForm

import requests_cache
import openmeteo_requests
from retry_requests import retry
import pandas as pd
import matplotlib.pyplot as plt
import os

# Create your views here.
def home(request):
  def make_graph(id):
    """
    IDs:
      Temperature: temperature_2m
    """
    params = {
      "latitude": location.latitude,
      "longitude": location.longitude,
      "hourly": id
      }

    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]

    print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
    print(f"Elevation {response.Elevation()} m asl")
    print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
    print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

    # Process hourly data. The order of variables needs to be the same as requested.
    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()

    hourly_data = {"date": pd.date_range(
      start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
      end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
      freq = pd.Timedelta(seconds = hourly.Interval()),
      inclusive = "left"
    )}

    hourly_data["temperature_2m"] = hourly_temperature_2m

    hourly_dataframe = pd.DataFrame(data = hourly_data)
    print(hourly_dataframe)
    #-----------------------------------------------------
    if id == "temperature_2m":
      title = "Temperature"
      y_label = "Temperature (°C)"
    elif id == "precipitation_probability":
      title = "Rain Probability"
      y_label = "Chance (%)"
    elif id == "wind_speed_10m":
      title = "Wind Speed"
      y_label = "Speed (km/h)"
    elif id == "snowfall":
        title = "Snowfall"
        y_label = "Meters"
    else:
      title = "Sunlight Exposure"
      y_label = "UV Index"
    plt.figure(figsize=(12, 6))
    plt.plot(hourly_dataframe["date"], hourly_dataframe["temperature_2m"], marker='o', linestyle='-', color='b', markersize=3)
    plt.xlabel("Time (UTC)")
    plt.ylabel(y_label)
    plt.title(title)
    plt.xticks(rotation=45, fontsize=8)
    plt.grid(True)


    image_path = "home/static/temperature_plot.png"

    plt.savefig(image_path, bbox_inches="tight")
    plt.close()




  #----------------------------------------------------------
  form = homeForm()
  if request.method == "POST":
    print(request.POST)
    form = homeForm(request.POST)
    if form.is_valid():
      print(form.cleaned_data)
      address = form.cleaned_data["address"]
      data_type = form.cleaned_data["data_type"]
      print("DATA TYPE: ", data_type)
      geolocator = Nominatim(user_agent="my_django_app")  

      location = geolocator.geocode(address)
      print(location.latitude, location.longitude)

      url = "https://api.open-meteo.com/v1/forecast"
      match data_type:
        case "3":
          make_graph("temperature_2m")
        case "1":
          make_graph("precipitation_probability")
        case "2":
          make_graph("uv_index")
        case "4":
          make_graph("wind_speed_10m")
        case "5":
          make_graph("snowfall")
        case _:
          print("Nothing")
      return render(request, "results/results.html", {"form": form, "image_path": "/static/temperature_plot.png"})
    else:
      return render(request, "home/home.html", {"form": form}) 
  else:
    form = homeForm()
  
  return render(request, "home/home.html", {"form": form})
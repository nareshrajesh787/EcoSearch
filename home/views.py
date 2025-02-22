from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from geopy.geocoders import Nominatim

from .forms import homeForm


# Create your views here.
def home(request):
  form = homeForm()
  if request.method == "POST":
    print(request.POST)
    form = homeForm(request.POST)
    if form.is_valid():
      print(form.cleaned_data)
      address = form.cleaned_data["address"]
      data_type = form.cleaned_data["data_type"]

      geolocator = Nominatim(user_agent="my_django_app")  

      location = geolocator.geocode(address)
      print(location.latitude, location.longitude)

      return render(request, "results/results.html", {"content": location})
      #add code to convert url to coordinates
      #then call second page with coords and data type as query string
    else:
      return render(request, "home/home.html", {"form": form}) 
  else:
    form = homeForm()
  
  return render(request, "home/home.html", {"form": form})

def graph_page(request):
  return HttpResponse()





def homeV2(request):
  form = homeForm()
  if request.method == "POST":
    print(request.POST)
    form = homeForm(request.POST)
    if form.is_valid():
      print(form.cleaned_data)
      address = form.cleaned_data["address"]
      data_type = form.cleaned_data["data_type"]

      geolocator = Nominatim(user_agent="my_django_app")  

      location = geolocator.geocode(address)
      print(location.latitude, location.longitude)

      return render(request, "home/home.html", {"content": location})
      #add code to convert url to coordinates
      #then call second page with coords and data type as query string
    else:
      return render(request, "home/home.html", {"form": form}) 
  else:
    form = homeForm()

  return render(request, "home/home (copy).html", {"form": form})

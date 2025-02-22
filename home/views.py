from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.urls.base import is_valid_path
from .forms import homeForm
from .models import addressModel

# Create your views here.
def home(request):
  form = homeForm()
  if request.method == "POST":
    form = homeForm(request.POST)
    if form.is_valid():
      address = form.POST["address"]
      data_type = form.POST["data_type"]
      new_address = addressModel(address=address)
      new_address.save()
      return redirect("list")
      
      #add code to convert url to coordinates
      #then call second page with coords and data type as query string
    else:
      return render(request, "home/home.html", {"form": form}) 
  else:
    form = homeForm()
  
  return render(request, "home/home.html", {"form": form})

def list(request):
  address = addressModel.objects.all()
  return render(request, "home/list.html", {"address": address})

def graph_page(request):
  return HttpResponse()
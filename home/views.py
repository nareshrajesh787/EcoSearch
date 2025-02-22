from django.http.response import HttpResponse
from django.shortcuts import render
from django.urls.base import is_valid_path
from .forms import homeForm

# Create your views here.
def home(request):
  if request.method == "POST":
    form = homeForm(request.POST)
    if form.is_valid():
      address = form.POST["address"]
      data_type = form.POST["data_type"]
      #add code to convert url to coordinates
      #then call second page with coords and data type as query string



def graph_page(request):
  return HttpResponse()
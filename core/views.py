from django.shortcuts import render
from fruits.models import FruitModel
from django.views.generic import DetailView
# Create your views here.
def home(request):
    data = FruitModel.objects.all()
    return render(request, 'home.html', {'data':data})


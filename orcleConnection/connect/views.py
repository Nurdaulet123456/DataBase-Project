from django.shortcuts import render

# Create your views here.
from .models import *
def index(request):
    return render(request, 'index.html', {'banks': Bank_card.objects.all(), 'discounts':Discounts.objects.all()})


def search(request):
    return render(request, 'search.html')

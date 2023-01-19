from django.shortcuts import render
from . import features


# Create your views here.

def welcome(request):
    return render(request, 'HongikMap/welcome.html', {})


def main(request):
    return render(request, 'HongikMap/main.html', {})

from django.shortcuts import render
from django.http import JsonResponse
from . import features


# Create your views here.

def welcome(request):
    return render(request, 'HongikMap/welcome.html', {})


def main(request):
    return render(request, 'HongikMap/main.html', {})


def main2(request):
    return render(request, 'HongikMap/main2.html', {})


def recommend(request):
    start_input = request.POST.get('start_input')
    end_input = request.POST.get()
    return JsonResponse({})

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
    response_name = request.POST.get('input_val')
    response_list = features.Recommend().find(response_name)
    print(response_name, response_list)
    return JsonResponse({response_name: response_list})


def submit(request):
    print("submit")
    departure = request.POST.get('departure')
    destination = request.POST.get('destination')

    elevatorUse = {'distance': 10, 'route': []}
    elevatorNoUse = {'distance': 15, 'route': []}
    return JsonResponse({'elevatorUse': elevatorUse, 'elevatorNoUse': elevatorNoUse})

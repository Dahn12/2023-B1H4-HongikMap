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
    response_list.sort()
    return JsonResponse({"recommendations": response_list})


def submit(request):
    departure = request.POST.get('departure')
    destination = request.POST.get('destination')
    departure_node, destination_node = features.recommend2node(departure), features.recommend2node(destination)

    elevatorUse = features.find_route_in_result(departure_node, destination_node, elevator=True)
    elevatorNoUse = features.find_route_in_result(departure_node, destination_node, elevator=False)
    return JsonResponse({'elevatorUse': elevatorUse, 'elevatorNoUse': elevatorNoUse})

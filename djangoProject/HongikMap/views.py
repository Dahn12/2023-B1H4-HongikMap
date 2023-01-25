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

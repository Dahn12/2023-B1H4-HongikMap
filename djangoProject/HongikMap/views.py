from django.shortcuts import render
from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt

from . import features
from . import suggest
from . import utility

# Create your views here.

def welcome(request):
    return render(request, 'HongikMap/welcome.html', {})


def main(request):
    return render(request, 'HongikMap/main.html', {})


def main2(request):
    return render(request, 'HongikMap/main2.html', {})


def recommend(request):
    response_name = request.POST.get('input_val')
    response_list = suggest.recommend(response_name)
    # response_list.sort(key=lambda x: (int(x[1:]) if str(x[1:]).isdecimal() else str(x[1:]), x[0]))
    return JsonResponse({"recommendations": response_list})


def submit(request):
    departure = request.POST.get('departure')
    destination = request.POST.get('destination')
    # departure_node, destination_node = features.recommend2node(departure), features.recommend2node(destination)

    departure_node = utility.recommend2node(departure)
    destination_node = utility.recommend2node(destination)

    elevatorUse = features.find_route_in_result(departure_node, destination_node, elevator=True)
    elevatorNoUse = features.find_route_in_result(departure_node, destination_node, elevator=False)

    return JsonResponse({'elevatorUse': elevatorUse, 'elevatorNoUse': elevatorNoUse})


def compute(request):
    graph_with_elevator = features.Graph()
    graph_without_elevator = features.Graph(elevator=False)

    path_with_elevator = features.Path(graph_with_elevator)
    path_without_elevator = features.Path(graph_without_elevator)

    for start in graph_with_elevator.rooms:
        path_with_elevator.dijkstra(start)

    with open("HongikMap/static/data/result_with_elevator.txt", "w", encoding="UTF8") as f:
        for key, value in path_with_elevator.result.items():
            f.write(f'{key[0]} {key[1]}:{value["distance"]} {" ".join(value["route"])}\n')

    for start in graph_without_elevator.rooms:
        path_without_elevator.dijkstra(start)
    with open("HongikMap/static/data/result_without_elevator.txt", "w", encoding="UTF8") as f:
        for key, value in path_without_elevator.result.items():
            f.write(f'{key[0]} {key[1]}:{value["distance"]} {" ".join(value["route"])}\n')

    with open("HongikMap/static/data/recommends_by_parsing.txt", "w", encoding="UTF8") as f:
        for room in path_with_elevator.rooms:
            building, floor, entity = room.split("-")
            f.write(f'{room}:{building + floor}{entity:0>2},{building}동 {floor}층 {entity}호\n')

    return render(request, 'HongikMap/welcome.html', {})

from django.apps import AppConfig
from . import features


class HongikmapConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'HongikMap'

    graph_with_elevator = features.Graph()
    graph_without_elevator = features.Graph(elevator=False)

    path_with_elevator = features.Path(graph_with_elevator)
    path_without_elevator = features.Path(graph_without_elevator)

    for start in graph_with_elevator.rooms:
        path_with_elevator.dijkstra(start)

    with open("HongikMap/static/data/result_with_elevator.txt", "w") as f:
        for key, value in path_with_elevator.result.items():
            f.write(f'{key[0]} {key[1]}:{value["distance"]} {" ".join(value["route"])}\n')

    for start in graph_without_elevator.rooms:
        path_without_elevator.dijkstra(start)
    with open("HongikMap/static/data/result_without_elevator.txt", "w") as f:
        for key, value in path_without_elevator.result.items():
            f.write(f'{key[0]} {key[1]}:{value["distance"]} {" ".join(value["route"])}\n')

    with open("HongikMap/static/data/recommends_by_parsing.txt", "w", encoding="UTF8") as f:
        for room in path_with_elevator.rooms:
            building, floor, entity = room.split("-")
            f.write(f'{room}:{building + floor}{entity:0>2},{building}동 {floor}층 {entity}호\n')


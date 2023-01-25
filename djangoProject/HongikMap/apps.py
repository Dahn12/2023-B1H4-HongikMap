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
            f.write(f'{key} {value}')

    for start in graph_without_elevator.rooms:
        path_without_elevator.dijkstra(start)
    with open("HongikMap/static/data/result_without_elevator.txt", "w") as f:
        for key, value in path_without_elevator.result.items():
            f.write(f'{key} {value}')

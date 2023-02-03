from .utility import *
import heapq


def update() -> None:
    graph_with_elevator = Graph(elevator=True)
    graph_without_elevator = Graph(elevator=False)

    path_with_elevator = Path(graph_with_elevator)
    path_without_elevator = Path(graph_without_elevator)

    for start in path_with_elevator.rooms:
        path_with_elevator.dijkstra(start)

    with open(result_with_elevator_path, "w", encoding="UTF8") as f:
        for key, value in path_with_elevator.result.items():
            f.write(f'{key[0]} {key[1]}:{value["distance"]} {" ".join(value["route"])}\n')

    for start in path_without_elevator.rooms:
        path_without_elevator.dijkstra(start)

    with open(result_without_elevator_path, "w", encoding="UTF8") as f:
        for key, value in path_without_elevator.result.items():
            f.write(f'{key[0]} {key[1]}:{value["distance"]} {" ".join(value["route"])}\n')

    with open(recommends_by_parsing_path, "w", encoding="UTF8") as f:
        for room in path_with_elevator.rooms:
            building, floor, entity = room.split("-")
            f.write(f'{room}:{building + floor}{entity:0>2},{building}동 {floor}층 {entity}호\n')


class Graph:
    def __init__(self, elevator: bool):
        self.rooms = []
        self.nodes = []
        self.weights = []
        self.useless = []

        with open(data_path, "r", encoding="UTF8") as f:
            for line in f.readlines():
                equality = False
                line_length = len(line.split())

                if invalid_line_for_update(line):
                    self.useless.append(line)
                    continue

                if line_length == 4 and line.split()[3] == "t":
                    equality = True

                print("Read | " + line)

                start, end, weight = line.split()[:3]
                weight = int(weight)

                if invalid_node(start) or invalid_node(end):
                    self.useless.append(line)
                    continue

                if not elevator:
                    if is_elevator(start) or is_elevator(end):
                        continue

                self.insert_node(start)
                self.insert_node(end)

                if (start, end, weight) not in self.weights:
                    self.weights.append((start, end, weight))
                else:
                    self.useless.append("duplicated: " + line)

                if equality:
                    if (end, start, weight) not in self.weights:
                        self.weights.append((end, start, weight))
                    else:
                        self.useless.append("duplicated: " + line)

    def insert_node(self, node: str):
        if node not in self.nodes:
            self.nodes.append(node)

        if is_room(node) and node not in self.rooms:
            self.rooms.append(node)


def invalid_line_for_update(line: str) -> bool:
    if "#" in line:
        return True

    line_length = len(line.split())
    if line_length not in [3, 4]:
        return True

    return False


def invalid_node(node: str) -> bool:
    if len(node.split("-")) != 3:
        return True
    return False


class Path:
    def __init__(self, graph: Graph):
        self.nodes = graph.nodes
        self.weights = graph.weights
        self.rooms = graph.rooms
        self.result = dict()

    def dijkstra(self, start):
        path = {key: {'distance': 1e9 if key != start else 0, 'parent': key} for key in self.nodes}

        graph = {key: [] for key in self.nodes}
        for key in graph:
            for _, adj, weight in filter(lambda x: x[0] == key, self.weights):
                graph[key].append((adj, weight))

        q = []
        heapq.heappush(q, (0, start))

        while q:
            dist, now = heapq.heappop(q)
            if path[now]['distance'] < dist:
                continue

            for adj, weight in graph[now]:
                cost = dist + weight
                if cost < path[adj]['distance']:
                    path[adj]['distance'] = cost
                    path[adj]['parent'] = now
                    heapq.heappush(q, (cost, adj))

        self.store(start, path)

    def store(self, start: str, path: dict):
        for end in self.rooms:
            route = [end]
            print(start, end)
            while route[-1] != start:
                route.append(path[route[-1]]['parent'])
            self.result[(start, end)] = {'distance': path[end]['distance'], 'route': route[::-1]}

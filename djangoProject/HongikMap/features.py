import heapq
from collections import OrderedDict


class Recommend:
    def __init__(self):
        self.recommends = dict()
        self.keywords = dict()

    def find(self, keyword: str):

        ret = self.find_in_keywords(keyword)
        kw_length = len(keyword)
        if kw_length <= 0:
            return ret
        if not ret:
            ret = self.find_by_parsing(keyword)

        # if keyword[0].encode().isalpha():  # 첫 글자가 영어: I101
        #
        #     ret = self.find_by_parsing(keyword)
        # elif keyword.isdecimal():  # 전체가 숫자: 101
        #
        #     ret = self.find_in_keywords(keyword)
        # else:  # 한글 입력: 카나
        #
        #     ret = self.find_in_keywords(keyword)
        return ret

    def find_by_parsing(self, keyword):
        ret = []

        with open("HongikMap/static/data/recommends_by_parsing.txt", "r", encoding="UTF8") as rec:
            for line in rec.readlines():
                key, recommends = line.split(":")
                recommends = recommends.split(",")
                if any([keyword in x for x in recommends]):
                    ret.append(recommends[0])
        return ret

    def find_in_keywords(self, keyword):
        ret = []
        # keywords 만 찾음
        with open("HongikMap/static/data/keywords.txt", "r", encoding="UTF8") as rec:
            for line in rec.readlines():
                key, recommends = line.split(":")
                recommends = recommends.split(",")
                if any([keyword in x for x in recommends]):
                    ret.append(recommends[0])
        return ret


class Graph:
    def __init__(self, elevator: bool = True):
        self.rooms = []
        self.nodes = []
        self.weights = []
        self.useless = []
        with open("HongikMap/static/data/data.txt", "r") as f:
            for line in f.readlines():
                equality = False
                line_length = len(line.split())
                if "#" in line or line_length not in [3, 4]:
                    self.useless.append(line)
                    continue

                if line_length == 4 and line.split()[3] == "t":
                    equality = True
                start, end, weight = line.split()[:3]
                weight = int(weight)

                if self.check_invalidity(start, line) or self.check_invalidity(end, line):
                    continue

                if not elevator:
                    if self.contains_elevator(start) or self.contains_elevator(end):
                        continue

                self.verify_and_insert(start)
                self.verify_and_insert(end)

                if (start, end, weight) not in self.weights:
                    self.weights.append((start, end, weight))
                else:
                    self.useless.append("duplicated: " + line)
                if equality:
                    if (end, start, weight) not in self.weights:
                        self.weights.append((end, start, weight))
                else:
                    self.useless.append("duplicated" + line)

    def check_invalidity(self, node: str, line):
        if len(node.split("-")) != 3:
            self.useless.append(line)
            return True
        return False

    def verify_and_insert(self, node):
        building, floor, entity = node.split("-")

        if node not in self.nodes:
            self.nodes.append(node)

        if node not in self.rooms and entity.isdecimal():
            self.rooms.append(node)

    def contains_elevator(self, node: str):
        building, floor, entity = node.split("-")
        return entity[0] == "E"


class Path:
    def __init__(self, graph: Graph):
        self.nodes = graph.nodes
        self.weights = graph.weights
        self.rooms = graph.rooms
        self.result = dict()

    def dijkstra(self, start: str):
        path = {key: {'distance': 1e9 if key != start else 0, 'parent': key} for key in self.nodes}

        graph = {key: [] for key in self.nodes}
        for key in graph:
            # for k, w in self.weights.items():
            #     if k[0] == key:
            #         graph[key].append((k[1], w))

            # for (_, adj), weight in filter(lambda x: x[0][0] == key, self.weights.items()):
            #     graph[key].append((adj, weight))

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
            while route[-1] != start:
                route.append(path[route[-1]]['parent'])
            self.result[(start, end)] = {'distance': path[end]['distance'], 'route': route[::-1]}

    def find(self, start, end):
        return self.result[(start, end)]


def recommend2node(user_input: str):
    with open("HongikMap/static/data/keywords.txt", "r", encoding="UTF8") as f:
        for line in f.readlines():
            node, recommend = line.split(":")
            if user_input == recommend.split(",")[0]:
                return node

    with open("HongikMap/static/data/recommends_by_parsing.txt", "r", encoding="UTF8") as f:
        for line in f.readlines():
            node, recommend = line.split(":")
            if user_input == recommend.split(",")[0]:
                return node

    return ""


def node2recommend(nodes: list):
    nodes = compress_nodes(nodes)

    result = OrderedDict()
    for node in nodes:
        result[node] = ""

    with open("HongikMap/static/data/keywords.txt", "r", encoding="UTF8") as f:
        for line in f.readlines():
            node, value = line.split(":")
            if node in nodes:
                result[node] = value.split(",")[0]
                nodes.remove(node)
                if not nodes:
                    break

    for node in result.keys():
        if result[node] == "":
            result[node] = convert_into_keyword(node)
    # with open("HongikMap/static/data/recommends_by_parsing.txt", "r", encoding="UTF8") as f:
    #     for line in f.readlines():
    #         node, value = line.split(":")
    #         if node in nodes:
    #             result[node] = value.split(",")[0]
    #             nodes.remove(node)
    #             if not nodes:
    #                 break
    # for key, value in result.items():
    #    print(key, value)
    return list(result.values())


def compress_nodes(nodes: list):
    nodes = compress_hallway(nodes)
    nodes = compress_elevator_and_stair(nodes)
    return nodes


def compress_hallway(nodes: list):
    result = [nodes[0]]
    for node in nodes[1:]:
        if is_hallway(node) and same_kind(result[-1], node):
            pass
        else:
            result.append(node)
    return result


def is_hallway(node: str):
    return node.split("-")[2][0] == "H"


def same_kind(prev, cur):
    prev_entity, cur_entity = prev.split("-")[2], cur.split("-")[2]
    return prev_entity[0] == cur_entity[0]


def compress_elevator_and_stair(nodes: list):
    result = [nodes[0]]
    prev = ""
    for node in nodes[1:]:
        if not same_kind(result[-1], node):
            if prev != "":
                result.append(prev)
                prev = ""
            result.append(node)
        elif node.split("-")[2][0] in ["S", "E"]:
            prev = node

    return result


def convert_into_keyword(node: str):
    building, floor, entity = node.split("-")
    if entity[0] == "E":
        return "{}동 {}층 {}".format(building, floor, "엘리베이터")
    elif entity[0] == "H":
        return "{}동 {}층 {}".format(building, floor, "복도")
    elif entity[0] == "S":
        return "{}동 {}층 {}".format(building, floor, "계단")
    elif entity[0] == "X":
        return "{}동 {}층 {}".format(building, floor, "출입문")
    elif entity.isdecimal():
        return f'{building + floor}{entity:0>2}'
    else:
        return node


def find_route_in_result(departure, destination, elevator):
    result_path = ""
    if elevator:
        result_path = "HongikMap/static/data/result_with_elevator.txt"
    else:
        result_path = "HongikMap/static/data/result_without_elevator.txt"
    with open(result_path, "r") as f:
        for line in f.readlines():
            pair, value = line.split(":")
            pair = tuple(pair.split())
            value = value.split()
            if (departure, destination) == pair:
                coordinates = get_coordinates(value[1:])
                distance, route = value[0], node2recommend(value[1:])
                # print(route)
                return {"distance": distance, "route": route, "coordinates": coordinates}


def get_coordinates(nodes: list):
    result = OrderedDict()
    for node in nodes:
        if valid_external_node(node):
            result[node] = []

    with open("HongikMap/static/data/coordinate.txt", "r") as f:
        for line in f.readlines():
            if "#" in line:
                continue

            name, x, y = line.split()
            if name in result.keys():
                result[name] = [x, y]

    return list(result.values())


def valid_external_node(node: str):
    building, floor, entity = node.split("-")

    return entity[0] in ["X", "E", "S"]

import heapq
from collections import OrderedDict


class Recommend:
    def find(self, keyword: str):

        ret = []
        kw_length = len(keyword)
        if kw_length <= 0:
            return ret

        keyword_list = self.find_in_keywords(keyword)
        parsing_list = self.find_by_parsing(keyword)
        sorted_parsing_list = self.sort_parsing_list(parsing_list)
        ret = keyword_list + sorted_parsing_list
        # if not ret:
        #    ret = self.find_by_parsing(keyword)

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

    def find_by_parsing(self, keyword):
        ret = []

        with open("HongikMap/static/data/recommends_by_parsing.txt", "r", encoding="UTF8") as rec:
            for line in rec.readlines():
                key, recommends = line.split(":")
                recommends = recommends.split(",")
                if any([keyword in x for x in recommends]):
                    ret.append((key, recommends[0]))
        return [x[1] for x in sorted(ret, key=lambda x: x[0])]

    def sort_parsing_list(self, parsing_list: list):
        underground = list(filter(lambda x: x[1] == "B", parsing_list))
        ground = list(set(parsing_list) - set(underground))

        underground.sort(key=lambda x: int(x[2:]))
        ground.sort(key=lambda x: int(x[1:]))
        return underground + ground


class Graph:
    def __init__(self, f, elevator: bool = True):
        self.exits = []
        self.rooms = []
        self.nodes = []
        self.weights = []
        self.useless = []
        #파일의 첫부분부터 읽도록 포인터 조정
        f.seek(0)
        # read()는 전체 읽기 readline은 한줄읽기, readlines는 줄별로 리스트로 만들어준다.


        for line in f.readlines():
            # 현재 읽는 줄을 출력
            print("Read | " + line)
            # equality는 방향, 무방향 체크
            equality = False

            #형식체크
            # 줄에 #이 있거나 길이가 3혹은 4가 아닌경우 쓸모없는 리스트에 추가하고 다음줄로 넘어간다.
            # split는 기본적으로 whitespace단위로 최대한 나눈다.
            line_length = len(line.split())
            if "#" in line or line_length not in [3, 4]:
                self.useless.append(line)
                continue
            # 만약 개수가 4개이고(출발지,도착지, 가중치,방향성) 마지막원소가 t이면 무방향이며, equlity트루로
            if line_length == 4 and line.split()[3] == "t":
                equality = True
            # 출발지 도착지 유효성 체크
            start, end, weight = line.split()[:3]
            weight = float(weight)
            if self.check_invalidity(start, line) or self.check_invalidity(end, line):
                continue
            # 처음에 elevator가 False(미사용)이면 출발지, 도착지 중 하나라도 E이면 제외
            if not elevator:
                if self.is_elevator(start) or self.is_elevator(end):
                    continue

            self.verify_and_insert(start)
            self.verify_and_insert(end)
            # 출발.도착,가중치를 묶은 튜플이 weights에 없을때
            if (start, end, weight) not in self.weights:
                self.weights.append((start, end, weight))
            else:
                self.useless.append("duplicated: " + line)
            #만약 방향성이 있을때 출발지와 도착지를 뒤집어서 다시 넣어준다.
            if equality:
                if (end, start, weight) not in self.weights:
                    self.weights.append((end, start, weight))
            else:
                self.useless.append("duplicated: " + line)

    # 각 출발지와 도착지정보가 노드형식에 맞는지 체크한 다음 잘못된 형식이면 useless에 추가하고 True반환
    def check_invalidity(self, node: str, line):
        if len(node.split("-")) != 3:
            self.useless.append(line)
            return True
        return False

    # 출발지와 도착지가 nodes에 없으면 넣어주기
    def verify_and_insert(self, node):
        building, floor, entity = node.split("-")

        if node not in self.nodes:
            self.nodes.append(node)
        # rooms에 노드가 없고, 3번째인자가 숫자로만(강의실 혹은 외부위치)구성되어있으며, 이것이 외부노드가 아닐 떄 (전체적으로 강의실일때) rooms에 추가
        if node not in self.rooms:
            self.rooms.append(node)
        if node not in self.rooms and entity[0] == 'X' or entity[0] == 'x':
            self.exits.append(node)

    # E인지 체크
    def is_elevator(self, node: str):
        building, floor, entity = node.split("-")
        return entity[0] == "E"


# 가지고 온 그래프에 대한 경로를 개선
class Path:
    def __init__(self, graph: Graph):
        self.exits = graph.exits
        self.nodes = graph.nodes
        self.weights = graph.weights
        self.rooms = graph.rooms
        self.result = dict()

    def dijkstra(self, start: str):
        # 가중치 최대 10억(1e9) 출발지와 같지 않은 모든 장소(노드)는 모두 10억을 준다. 만약 같으면 0을 준다.
        path = {key: {'distance': 1e9 if key != start else 0, 'parent': key} for key in self.nodes}
        # graph리스트는 특정노드에서 갈 수 있는 노드와 가중치에 대한 리스트
        graph = {key: [] for key in self.nodes}
        for key in graph:
            # for k, w in self.weights.items():
            #     if k[0] == key:
            #         graph[key].append((k[1], w))

            # for (_, adj), weight in filter(lambda x: x[0][0] == key, self.weights.items()):
            #     graph[key].append((adj, weight))

            # weights라는 리스트에 대하여 출발지가 나 자신일 때 그 인접 노드에 대해 가중치와 함께 저장
            for _, adj, weight in filter(lambda x: x[0] == key, self.weights):
                graph[key].append((adj, weight))
        # q는 우선순위 리스트
        q = []
        # q라는 우선순위 리스트에 (0,start)를 넣고 다익스트라 시작
        heapq.heappush(q, (0, start))

        while q:
            # 우선순위 큐에서 가장 가중치가 작은 것을 뺴면서 이에 대한 거리, 위치를 지정해 여기서 가중치 갱신
            dist, now = heapq.heappop(q)
            # 만약 현재 저장되어있는 거리가 큐에 담아둔 거리보다 작은경우 최단거리가 아니므로 패스
            if path[now]['distance'] < dist:
                continue
            # 거리가 더 짧을경우 그 노드를 방문하게 되고 출발지에서 그 노드를 거쳐 인접노드까지 거리를 갱신
            for adj, weight in graph[now]:
                cost = dist + weight
                if cost < path[adj]['distance']:
                    path[adj]['distance'] = cost
                    # 출발지에서 경로를 표시하기위해 노드에 이전 노드를 저장
                    path[adj]['parent'] = now
                    heapq.heappush(q, (cost, adj))

        self.store(start, path)

    def store(self, start: str, path: dict):
        for end in self.rooms + self.exits:
            route = [end]
            print(start, end)
            # route의 마지막이 시작점이 될때까지 중간경로를 계속해서 넣어준다. 즉 route는 마지막 장소부터 역순으로 들어간다.
            while route[-1] != start:
                # 넣은 것의 parent를 계속해서 붙여준다.
                route.append(path[route[-1]]['parent'])
                # 리스트[start:end:step] step만큼 건너뛴다.
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


    # with open("HongikMap/static/data/recommends_by_parsing.txt", "r", encoding="UTF8") as f:
    #     for line in f.readlines():
    #         node, value = line.split(":")
    #         if node in nodes:
    #             result[node] = value.split(",")[0]
    #             nodes.remove(node)
    #             if not nodes:
    #                 break

    for node in result.keys():
        if result[node] == "":
            result[node] = convert_into_keyword(node)

    return list(result.values())


def compress_nodes(nodes: list):
    nodes = compress_hallway_and_external(nodes)
    nodes = compress_elevator_and_stair(nodes)
    return nodes


def compress_hallway_and_external(nodes: list):
    result = [nodes[0]]
    for node in nodes[1:]:
        if (is_hallway(node) or is_external(node)) and same_kind(result[-1], node):
            pass
        else:
            result.append(node)
    return result


def is_hallway(node: str):
    return node.split("-")[2][0] == "H"


def is_external(node: str):
    return node.startswith("외부")


def same_kind(prev, cur):
    prev_building, _, prev_entity = prev.split("-")
    cur_building, _, cur_entity = cur.split("-")
    return (prev_building == "외부" and cur_building == "외부") or prev_entity[0] == cur_entity[0]


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
    if floor[0] == "B":
        floor = "지하" + floor[1:]
    if entity[0] == "E":
        return "{}동 {}층 {}".format(building, floor, "엘리베이터")
    elif entity[0] == "H":
        return "{}동 {}층 {}".format(building, floor, "복도")
    elif entity[0] == "S":
        return "{}동 {}층 {}".format(building, floor, "계단")
    elif entity[0] == "X":
        return "{}동 {}층 {}".format(building, floor, "출입문")
    elif building == "외부":
        return "건물 외부"
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

    with open(result_path, "r", encoding="UTF8") as f:
        for line in f.readlines():
            pair, value = line.split(":")
            pair = tuple(pair.split())
            value = value.split()
            if (departure, destination) == pair:
                distance = value[0]

                compressed_route = compress_nodes(value[1:])
                route = node2recommend(compressed_route)
                coordinates = get_coordinates(value[1:])
                # print(route)
                return {"distance": distance, "route": route, "coordinates": coordinates}


def get_coordinates(nodes: list):
    result = OrderedDict()
    for node in nodes:
        if valid_external_node(node):
            if node.startswith("외부"):
                node = node.split("-")[2]
            result[node] = []

    # for x in result.items():
    #     print(x)

    with open("HongikMap/static/data/coordinate.txt", "r", encoding='UTF8') as f:
        for line in f.readlines():
            if "#" in line or len(line.split()) != 3:
                continue

            name, x, y = line.split()
            if name in result.keys():
                # print(f'coordinate added {name} : {(x, y)}')
                result[name] = [x, y]
    print("찾은 경로 좌표")
    for k, v in result.items():
        print(k, v)
    return list(result.values())


def valid_external_node(node: str):
    building, floor, entity = node.split("-")

    if building == "외부":
        return True
    if entity[0] in ["S", "E", "X"]:
        return True

    return False

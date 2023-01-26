import heapq


class Recommend:
    def __init__(self):
        self.recommends = dict()
        self.keywords = dict()

        with open("HongikMap/static/data/keywords.txt", "r", encoding='UTF8') as kw:
            for line in kw.readlines():
                entity, value = line.split(":")
                self.recommends[entity] = [x.rstrip() for x in value.split(",")]

        with open('HongikMap/static/data/recommends.txt', "r", encoding='UTF8') as rec:
            for line in rec.readlines():
                entity, value = line.split(":")
                self.keywords[entity] = value.rstrip()

    def find(self, keyword: str):

        ret = []
        kw_length = len(keyword)
        if kw_length <= 0:
            return ret

        if keyword[0].encode().isalpha():  # 첫 글자가 영어: I101
            print("input is alpha")
            ret = self.find_by_parsing(keyword)
        elif keyword.isdecimal():  # 전체가 숫자: 101
            print("전체숫자")
            ret = self.find_in_recommend(keyword)
        else:  # 한글 입력: 카나
            print("복합 입력")
            ret = self.find_in_recommend(keyword)
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

    def find_in_recommend(self, keyword):
        ret = []

        with open("HongikMap/static/data/keywords.txt", "r", encoding="UTF8") as rec:
            for line in rec.readlines():
                key, recommends = line.split(":")
                recommends = recommends.split(",")
                if any([keyword in x for x in recommends]):
                    ret.append(recommends[0])

        # if not ret:
        #     if keyword[0].isalpha() and keyword[0] != "Z":
        #         pass

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

                self.verify_and_insert(start)
                self.verify_and_insert(end)

                if (start, end, weight) not in self.weights:
                    self.weights.append((start, end, weight))
                if equality:
                    if (end, start, weight) not in self.weights:
                        self.weights.append((end, start, weight))

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

class Graph:
    def __init__(self):
        self.rooms = []
        self.nodes = []
        self.weights = []
        self.useless = []

        with open("../data.txt", "r") as f:
            for line in f.readlines():
                if "#" in line:
                    self.useless.append(line)
                    continue
                if len(line.split()) != 3:  # 한줄에 데이터가 start, end, weight로 나뉘지 않을 경우
                    self.useless.append(line)
                    continue

                start, end, weight = line.split()
                weight = int(weight)

                if self.check_invalidity(start):
                    self.useless.append(start)
                    continue
                if self.check_invalidity(end):
                    self.useless.append(end)
                    continue

                self.verify_and_insert(start)
                self.verify_and_insert(end)

                if (start, end, weight) not in self.weights:
                    self.weights.append((start, end, weight))

    def check_invalidity(self, node: str) -> bool:
        return len(node.split("-")) != 3

    def verify_and_insert(self, node: str):
        building, floor, entity = node.split("-")

        if node not in self.nodes:
            self.nodes.append(node)

        if node not in self.rooms and entity.isdecimal():
            self.rooms.append(node)

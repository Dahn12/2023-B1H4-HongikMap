from collections import OrderedDict


def recommend2node(input_recommend: str):
    with open("HongikMap/static/data/keywords.txt", "r", encoding="UTF8") as f:
        for line in f.readlines():
            node, recommend = line.split(":")
            if input_recommend == recommend.split(",")[0]:
                return node

    with open("HongikMap/static/data/recommends_by_parsing.txt", "r", encoding="UTF8") as f:
        for line in f.readlines():
            node, recommend = line.split(":")
            if input_recommend == recommend.split(",")[0]:
                return node

    return ""


def nodes2recommends(input_nodes: list):
    result = OrderedDict()

    for node in input_nodes:
        result[node] = ""

    with open("HongikMap/static/data/keywords.txt", "r", encoding="UTF8") as f:
        for line in f.readlines():
            node, value = line.split(":")
            if node in input_nodes:
                result[node] = value.split(",")[0]
                input_nodes.remove(node)
                if not input_nodes:
                    break

    with open("HongikMap/static/data/recommends_by_parsing.txt", "r", encoding="UTF8") as f:
        for line in f.readlines():
            node, value = line.split(":")
            if node in input_nodes:
                result[node] = value.split(",")[0]
                input_nodes.remove(node)
                if not input_nodes:
                    break

    return list(result.values())


def node2keyword():
    pass
from collections import OrderedDict

EXTERNAL = "외부"
HALLWAY = "H"
ELEVATOR = "E"
STAIR = "S"
EXIT = "X"
BASEMENT = "B"


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

    # with open("HongikMap/static/data/recommends_by_parsing.txt", "r", encoding="UTF8") as f:
    #     for line in f.readlines():
    #         node, value = line.split(":")
    #         if node in input_nodes:
    #             result[node] = value.split(",")[0]
    #             input_nodes.remove(node)
    #             if not input_nodes:
    #                 break

    for node in result.keys():
        if result[node] == "":
            result[node] = node2keyword(node)

    return list(result.values())


def get_recommends(recommend_path: str, search_nodes: list) -> (dict, list):
    result = dict()
    with open(recommend_path, "r", encoding='UTF8') as f:
        for line in f.readlines():
            node, value = line.split(":")
            if node in search_nodes:
                result[node] = value.split(",")[0]
                search_nodes.remove(node)
                if not search_nodes:
                    break

    return result, search_nodes


def node2keyword(node: str) -> str:
    pass


# Return True if the node is at EXTERNAL
def is_external(node: str) -> bool:
    return node.startswith(EXTERNAL)


# Return True if entity of the node is hallway
def is_hallway(node: str) -> bool:
    return node.split("-")[2][0] == HALLWAY


# Return Ture if entity of the node is elevator
def is_elevator(node: str) -> bool:
    return node.split("-")[2][0] == ELEVATOR


# Return True if entity of the node is stair
def is_stair(node: str) -> bool:
    return node.split("-")[2][0] == STAIR


# Return True if entity of the node is exit
def is_exit(node: str) -> bool:
    return node.split("-")[2][0] == EXIT

def is_underground(node:str) -> bool:
    return node.split("-")[1].startswith()

def get_attribute(node: str) -> str:
    if is_external(node):
        return EXTERNAL

    if is_hallway(node):
        return HALLWAY

    if is_elevator(node):
        return ELEVATOR

    if is_stair(node):
        return STAIR

    if is_exit(node):
        return EXIT

    return "WRONG_NODE"


def same_kind(prev_node: str, cur_node: str) -> bool:
    if is_external(prev_node) and is_external(cur_node):
        return True

    if get_attribute(prev_node) == get_attribute(cur_node):
        return True

    return False

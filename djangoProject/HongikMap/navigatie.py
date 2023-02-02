from .utility import *


def search(departure: str, destination: str, elevator: bool) -> dict:
    result_path = get_result_path(elevator)

    with open(result_path, "r", encoding="UTF8") as f:
        for line in f.readlines():
            pair, value = line.split(":")

            pair = tuple(pair.split())
            value = value.split()

            if (departure, destination) == pair:
                distance = value[0]
                nodes = value[1:]

                compressed_route = get_compressed_route(nodes)
                route = utility.nodes2recommends(compressed_route)


def get_result_path(elevator: bool) -> str:
    if elevator:
        return "HongikMap/static/data/result_with_elevator.txt"
    else:
        return "HongikMap/static/data/result_without_elevator.txt"


def get_compressed_route(nodes: list) -> list:
    nodes = compress_hallway_and_external(nodes)
    nodes = compress_elevator_and_stair(nodes)

    return nodes


def compress_hallway_and_external(nodes: list) -> list:
    result = [nodes[0]]
    for node in nodes[1:]:
        if (is_hallway(node) or is_external(node)) and same_kind(node[-1], node):
            pass
        else:
            result.append(node)
    return result


def compress_elevator_and_stair(nodes: list) -> list:
    result = [nodes[0]]
    prev = ""
    for node in nodes[1:]:
        if not same_kind(result[-1], node):
            if prev != "":
                result.append(prev)
                prev = ""
            result.append(node)
        elif is_stair(node) or is_elevator(node):
            prev = node

    return result


def get_coordinates():
    pass

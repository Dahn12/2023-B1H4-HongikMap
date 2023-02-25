from .utility import *
from . import models


# 다익스트라 결과 파일에서 출발지와 도착지에 해당하는 경로를 찾아온다.
def search(departure: str, destination: str, elevator: bool) -> dict:
    # sending_dic는 딕셔너리이고 키로는  출발지도착지, 경로가 들어있고, 경로를 결과경로 간소화 시키고 좌표를 얻어 추가해서 리턴한다.
    sending_dic = models.get_route(departure, destination, elevator)
    sending_dic['coordinates'] = get_coordinates(sending_dic['route'])
    # 압축경로 만들기
    compressed_route = get_compressed_route(sending_dic['route'])
    sending_dic['route'] = nodes2recommends(compressed_route)
    # 노드 얻기

    return sending_dic
    # with open(result_path, "r", encoding="UTF8") as f:
    #     for line in f.readlines():
    #         pair, value = line.split(":")
    #         # 출발지,도착지를 pair에 담고 이를 튜플화하고 그걸다시 pair에 담는다.recommend.strip(' ')
    #         pair = tuple(pair.split())
    #
    #         value = value.split()
    #
    #         if (departure, destination) == pair:
    #             distance = value[0]
    #             nodes = value[1:]
    #
    #             compressed_route = get_compressed_route(nodes)
    #             route = nodes2recommends(compressed_route)
    #
    #             coordinates = get_coordinates(nodes)


def get_result_path(elevator: bool) -> str:
    if elevator:
        return result_with_elevator_path
    else:
        return result_without_elevator_path

# 경로중 건물복도이동, 엘리베이터 이동등 축소
def get_compressed_route(nodes: list) -> list:
    nodes = compress_hallway_and_external(nodes)
    nodes = compress_elevator_and_stair(nodes)

    return nodes


def compress_hallway_and_external(nodes: list) -> list:
    result = [nodes[0]]
    for node in nodes[1:]:
        if (is_hallway(node) or is_external(node)) and same_kind(result[-1], node):
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


def get_coordinates(nodes: list) -> list:
    result = OrderedDict()
    for node in nodes:
        if valid_node_for_coordinate(node):
            if is_external(node):
                node = get_external_node_number(node)
            result[node] = []

    with open(coordinate_path, "r", encoding='UTF8') as f:
        for line in f.readlines():
            if invalid_line_for_coordinate(line):
                continue

            name, x, y = line.split()
            if name in result.keys():
                result[name] = [x, y]

    return list(result.values())


def valid_node_for_coordinate(node: str) -> bool:
    if is_external(node):
        return True

    if get_kind(node) in ["S", "E", "X"]:
        return True

    return False


def invalid_line_for_coordinate(line: str) -> bool:
    if "#" in line:
        return True

    if len(line.split()) != 3:
        return True

    return False

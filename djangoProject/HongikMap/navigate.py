from .utility import *
from . import models


# 다익스트라 결과 파일에서 출발지와 도착지에 해당하는 경로를 찾아온다.
def search(departure: str, destination: str, elevator: bool) -> dict:
    result = {}
    minimum_route = {}
    # 경로가 DB에 있을경우 바로가져온다
    if models.exist_route(departure, destination, elevator):
        minimum_route = models.get_route(departure, destination, elevator)
    # DB에 경로가 없을경우 셋으로 나눠서 가져와야한다.
    if not models.exist_route(departure, destination, elevator):
        start_to_exit = models.get_routes_of_start_building(departure, elevator)
        exit_to_end = models.get_routes_of_end_building(destination, elevator)
        merged_route = []

        for start_route in start_to_exit:
            for end_route in exit_to_end:
                exit_to_exit = models.get_route(start_route['route'][-1], end_route['route'][0], elevator)
                distance = start_route['distance'] + exit_to_exit['distance'] + end_route['distance']
                route = start_route['route'] + exit_to_exit['route'][1:-1] + end_route['route']
                merged_route.append({
                    'distance': distance,
                    'route': route
                })
        minimum_route = sorted(merged_route, key=lambda x: x['distance'])[0]

        # 건물 안 경로 만들어주는함수
        new_minimum_route = minimum_route['route']
        for number in range(len(minimum_route['route']) - 1):
            if minimum_route['route'][number].split('-')[2][0] == 'X' and minimum_route['route'][number + 1].split('-')[2][0] == 'X':

                print(minimum_route['route'][number + 1].split('-')[2])
                # minimum_route에서 XtoX를찾으면 경로를 XtoX.txt에서 가져와야 한다.
                if elevator:
                    f = open('external_node/result_with_elevator_XtoX.txt', 'r', encoding="UTF8")
                else:
                    f = open('external_node/result_with_elevator_XtoX.txt', 'r', encoding="UTF8")
                for line in f.readlines():

                    intermediate_place1 = line.split(':')[0].split(' ')[0]
                    intermediate_place2 = line.split(':')[0].split(' ')[1]
                    XtoX_route = line.split(':')[1].split(' ')[2:-1]
                    if intermediate_place1 == minimum_route['route'][number] and intermediate_place2 == minimum_route['route'][number + 1]:
                        new_minimum_route[number + 1:number + 1] = XtoX_route
        minimum_route['route'] = new_minimum_route
    compressed_route = get_compressed_route(minimum_route['route'])
    result['distance'] = minimum_route['distance']
    result['route'] = nodes2recommends(compressed_route)
    result['coordinates'] = get_coordinates(minimum_route['route'])

    return result


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

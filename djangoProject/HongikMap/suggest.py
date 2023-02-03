from .utility import *


def recommend(keyword: str) -> list:
    keyword_length = len(keyword)
    if keyword_length <= 0:
        return []

    keyword_nodes = nodes_from_keywords(keyword)
    parsed_nodes = nodes_from_parsed(keyword)

    parsed_nodes = remove_duplicates(keyword_nodes, parsed_nodes)

    keyword_nodes.sort()
    parsed_nodes = sort_parsed_nodes(parsed_nodes)

    result = nodes2recommends(keyword_nodes + parsed_nodes)

    return result


def nodes_from_keywords(keyword: str) -> list:
    result = []
    with open(keywords_path, "r", encoding="UTF8") as f:
        for line in f.readlines():
            key, recommends = map(str, line.split(":"))
            recommends = recommends.split(",")
            if any([keyword in x for x in recommends]):
                result.append(key)
    return result


def nodes_from_parsed(keyword: str) -> list:
    result = []
    with open(recommends_by_parsing_path, "r", encoding="UTF8") as f:
        for line in f.readlines():
            key, recommends = map(str, line.split(":"))
            recommends = recommends.split(",")
            if any([keyword in x for x in recommends]):
                result.append(key)

    return result


def sort_parsed_nodes(parsed_nodes: list) -> list:
    underground = list(filter(lambda x: x.split("-")[1].startswith("B"), parsed_nodes))
    ground = list(set(parsed_nodes) - set(underground))

    underground.sort(key=lambda x: (int(x.split("-")[1][1:]), int(x.split("-")[2]), x[0]))
    ground.sort(key=lambda x: (int(x.split("-")[1]), int(x.split("-")[2]), x[0]))
    return underground + ground


def remove_duplicates(keyword_nods: list, parsed_nodes: list) -> list:
    result = list(set(parsed_nodes) - set(keyword_nods))

    return result

from django.db import models


# Create your models here.
def initialize_database():
    pass

def initialize_table():
    pass


def initialize_node_table():
    pass


def initialize_result_with_elevator_table():
    pass


def initialize_result_without_elevator_table():
    pass


def initialize_coordinate_table():
    pass


def clean():
    pass


def save_building(building: str, result: dict):
    pass


def get_route(node: str, elevator: bool) -> dict:
    pass


def get_coordinate(node: str) -> (int, int):
    pass

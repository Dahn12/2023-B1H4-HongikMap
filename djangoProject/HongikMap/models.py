from django.db import models


# Create your models here.
class Node(models.Model):
    node = models.CharField(max_length=30, primary_key=True)

    class Meta:
        db_table = 'node'


class ResultWithElevator(models.Model):
    class Meta:
        db_table = 'result_with_elevator'
        constraints = [
            models.UniqueConstraint(
                fields=["departure", "destination"],
                name="UniqueConstraintWithElevator",
            )
        ]

    departure = models.ForeignKey("Node", unique=False, primary_key=True, db_column='departure',
                                  on_delete=models.CASCADE, related_name='departure_with_elevator')
    destination = models.ForeignKey("Node", unique=False, db_column='destination',
                                    on_delete=models.CASCADE, related_name='destination_with_elevator')
    distance = models.IntegerField()
    route = models.CharField(max_length=1000)


class ResultWithoutElevator(models.Model):
    class Meta:
        db_table = 'result_without_elevator'
        constraints = [
            models.UniqueConstraint(
                fields=["departure", "destination"],
                name="UniqueConstraintWithoutElevator",
            )
        ]

    departure = models.ForeignKey("Node", unique=False, primary_key=True, db_column='departure',
                                  on_delete=models.CASCADE, related_name='departure_without_elevator')
    destination = models.ForeignKey("Node", unique=False, db_column='destination', on_delete=models.CASCADE,
                                    related_name='destination_without_elevator')
    distance = models.IntegerField()
    route = models.CharField(max_length=1000)


class Coordinate(models.Model):
    class Meta:
        db_table = 'coordinate'

    node = models.OneToOneField("Node", db_column='node', primary_key=True, on_delete=models.CASCADE,
                                related_name='coordinate_node')
    x = models.IntegerField()
    y = models.IntegerField()


def initialize_database():
    pass


def initialize_table():
    pass


def clean():
    pass


def save(result: dict, elevator: bool):
    print(f'Save New Data with{"" if elevator else "out"} elevator')

    if elevator:
        for (departure, destination), value in result.items():
            departure = Node(node=departure)
            destination = Node(node=destination)
            distance = value['distance']
            route = ','.join(value['route'])

            if not Node.objects.filter(node=departure.node).exists():
                departure.save()

            if not Node.objects.filter(node=destination.node).exists():
                destination.save()

            result_with_elevator = ResultWithElevator(departure=departure, destination=destination,
                                                      distance=distance, route=route)
            result_with_elevator.save()

    if not elevator:
        for (departure, destination), value in result.items():
            departure = Node(node=departure)
            destination = Node(node=destination)
            distance = value['distance']
            route = ','.join(value['route'])

            result_without_elevator = ResultWithoutElevator(departure=departure, destination=destination,
                                                            distance=distance, route=route)
            result_without_elevator.save()


def get_route(start: str, end: str, elevator: bool) -> dict:
    pass


def get_coordinate(node: str) -> (int, int):
    pass

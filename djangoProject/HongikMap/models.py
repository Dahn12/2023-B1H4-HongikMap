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

    departure = models.ForeignKey("Node", unique=False, db_column='departure',
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

    departure = models.ForeignKey("Node", unique=False, db_column='departure',
                                  on_delete=models.CASCADE, related_name='departure_without_elevator')
    destination = models.ForeignKey("Node", unique=False, db_column='destination',
                                    on_delete=models.CASCADE, related_name='destination_without_elevator')
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
    # print(f'Save New Data with{"" if elevator else "out"} elevator')

    if elevator:
        for (departure, destination), value in result.items():
            print(f'Save Data | {departure:10} {destination:10} elevator={elevator} ', end="")
            departure = Node(node=departure)
            destination = Node(node=destination)
            distance = value['distance']
            route = ','.join(value['route'])

            if not Node.objects.filter(node=departure.node).exists():
                departure.save()

            if not Node.objects.filter(node=destination.node).exists():
                destination.save()

            if ResultWithElevator.objects.filter(departure=departure, destination=destination).exists():
                print("update data")
                update_result = ResultWithElevator.objects.get(departure=departure, destination=destination)
                update_result.distance = distance
                update_result.route = route
                update_result.save()
            if not ResultWithElevator.objects.filter(departure=departure, destination=destination).exists():
                print("create node")
                result_with_elevator = ResultWithElevator(departure=departure, destination=destination,
                                                          distance=distance, route=route)
                result_with_elevator.save()

    if not elevator:
        for (departure, destination), value in result.items():
            print(f'Save Data | {departure:10} {destination:10} elevator={elevator} ', end="")
            departure = Node(node=departure)
            destination = Node(node=destination)
            distance = value['distance']
            route = ','.join(value['route'])

            if not Node.objects.filter(node=departure.node).exists():
                departure.save()
            if not Node.objects.filter(node=departure.node).exists():
                destination.save()
            if ResultWithoutElevator.objects.filter(departure=departure, destination=destination).exists():
                print("update node")
                update_result = ResultWithoutElevator.objects.get(departure=departure, destination=destination)
                update_result.distance = distance
                update_result.route = route
                update_result.save()
            if not ResultWithoutElevator.objects.filter(departure=departure, destination=destination).exists():
                print("create node")
                result_without_elevator = ResultWithoutElevator(departure=departure, destination=destination,
                                                                distance=distance, route=route)
                result_without_elevator.save()


def get_route(start: str, end: str, elevator: bool) -> dict:
    if not Node.objects.filter(node=start).exists() or not Node.objects.filter(node=end).exists():
        print('NonExistentNode: There is no such node')
        return {}
    departure = Node.objects.get(node=start)
    destination = Node.objects.get(node=end)

    if elevator:
        if not ResultWithElevator.objects.filter(departure=departure, destination=destination).exists():
            print('NonExistentRoute: There is no such route')
            return {}
        retrieved_route = ResultWithElevator.objects.get(departure=departure, destination=destination)
        distance = retrieved_route.distance
        route = retrieved_route.route.split(',')
        return {
            'distance': distance,
            'route': route
        }

    if not elevator:
        if not ResultWithoutElevator.objects.filter(departure=departure, destination=destination).exists():
            print('NonExistentRoute: There is no such route')
            return {}
        retrieved_route = ResultWithoutElevator.objects.get(departure=departure, destination=destination)
        distance = retrieved_route.distance
        route = retrieved_route.route.split(',')
        return {
            'distance': distance,
            'route': route
        }


def get_coordinate(node: str) -> (int, int):
    node = Node(node=node)
    if not Node.objects.filter(node=node.node).exists():
        node.save()
    if not Coordinate.objects.filter(node=node).exists():
        print('NonExistentCoordinate: There is no such coordinate')
        return ()

    return Coordinate.objects.filter(node=node).values()[0]

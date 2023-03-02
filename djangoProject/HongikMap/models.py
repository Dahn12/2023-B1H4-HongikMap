from django.db import models

NonExistentNode = '[NonExistentNode]: There is no such node'
NonExistentRoute = '[NonExistentRoute]: There is no such route'


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


class Recommendation(models.Model):
    class Meta:
        db_table = 'recommendation'

    node = models.OneToOneField("Node", db_column='node', primary_key=True, on_delete=models.CASCADE,
                                related_name='coordinate_node')
    recommendation = models.CharField(max_length=30)


def initialize_database():
    pass


def initialize_table():
    pass


def clean():
    pass


def save(result: dict, elevator: bool):
    # print(f'Save New Data with{"" if elevator else "out"} elevator')
    for (start, end), value in result.items():
        if not exist_node(start):
            Node(node=start).save()
        if not exist_node(end):
            Node(node=end).save()
        departure = Node.objects.get(node=start)
        destination = Node.objects.get(node=end)
        distance = value['distance']
        route = ','.join(value['route'])

        if exist_route(start, end, elevator):
            # print(f'update data | {start} {end} elevator={elevator}')
            update_result = None
            if elevator:
                update_result = ResultWithElevator.objects.get(departure=departure, destination=destination)
            if not elevator:
                update_result = ResultWithoutElevator.objects.get(departure=departure, destination=destination)
            update_result.distance = distance
            update_result.route = route
            update_result.save()
        if not exist_route(start, end, elevator):
            # print(f'create data | {start} {end} elevator={elevator}')
            if elevator:
                result_with_elevator = ResultWithElevator(departure=departure, destination=destination,
                                                          distance=distance, route=route)
                result_with_elevator.save()
            if not elevator:
                result_without_elevator = ResultWithoutElevator(departure=departure, destination=destination,
                                                                distance=distance, route=route)
                result_without_elevator.save()

    # if elevator:
    #     for (departure, destination), value in result.items():
    #         departure = Node(node=departure)
    #         destination = Node(node=destination)
    #         distance = value['distance']
    #         route = ','.join(value['route'])
    #
    #         if not Node.objects.filter(node=departure.node).exists():
    #             departure.save()
    #
    #         if not Node.objects.filter(node=destination.node).exists():
    #             destination.save()
    #
    #         if ResultWithElevator.objects.filter(departure=departure, destination=destination).exists():
    #             print(f'update data | {departure.node} {destination.node} elevator={elevator}')
    #             update_result = ResultWithElevator.objects.get(departure=departure, destination=destination)
    #             update_result.distance = distance
    #             update_result.route = route
    #             update_result.save()
    #         if not ResultWithElevator.objects.filter(departure=departure, destination=destination).exists():
    #             print(f'create data | {departure.node} {destination.node} elevator={elevator}')
    #             result_with_elevator = ResultWithElevator(departure=departure, destination=destination,
    #                                                       distance=distance, route=route)
    #             result_with_elevator.save()
    #
    # if not elevator:
    #     for (departure, destination), value in result.items():
    #         departure = Node(node=departure)
    #         destination = Node(node=destination)
    #         distance = value['distance']
    #         route = ','.join(value['route'])
    #
    #         if not Node.objects.filter(node=departure.node).exists():
    #             departure.save()
    #         if not Node.objects.filter(node=departure.node).exists():
    #             destination.save()
    #         if ResultWithoutElevator.objects.filter(departure=departure, destination=destination).exists():
    #             print(f'update data | {departure.node} {destination.node} elevator={elevator}')
    #             update_result = ResultWithoutElevator.objects.get(departure=departure, destination=destination)
    #             update_result.distance = distance
    #             update_result.route = route
    #             update_result.save()
    #         if not ResultWithoutElevator.objects.filter(departure=departure, destination=destination).exists():
    #             print(f'create data | {departure.node} {destination.node} elevator={elevator}')
    #             result_without_elevator = ResultWithoutElevator(departure=departure, destination=destination,
    #                                                             distance=distance, route=route)
    #             result_without_elevator.save()


def get_route(start: str, end: str, elevator: bool) -> dict:
    if not exist_node(start) or not exist_node(end):
        return {}
    departure = Node.objects.get(node=start)
    destination = Node.objects.get(node=end)

    if elevator:
        if not exist_route(start, end, elevator):
            print(f'NonExistentRoute: There is no such route | ({start}, {end})')
            return {}
        retrieved_route = ResultWithElevator.objects.get(departure=departure, destination=destination)
        distance = retrieved_route.distance
        route = retrieved_route.route.split(',')
        return {
            'distance': distance,
            'route': route
        }

    if not elevator:
        if not exist_route(start, end, elevator):
            print(f'NonExistentRoute: There is no such route | ({start}, {end})')
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


def get_routes_of_start_building(start: str, elevator: bool) -> list:
    if not exist_node(start):
        return []

    departure = Node.objects.get(node=start)
    if elevator:
        if not ResultWithElevator.objects.filter(departure=departure).exists():
            print(NonExistentRoute)
            return []
        routes = [{'distance': result['distance'], 'route': result['route'].split(',')} for result in
                  ResultWithElevator.objects.filter(departure=departure, destination__node__contains='X').values()]
        return routes
    if not elevator:
        if not ResultWithoutElevator.objects.filter(departure=departure).exists():
            print(NonExistentRoute)
            return []
        routes = [{'distance': result['distance'], 'route': result['route'].split(',')} for result in
                  ResultWithoutElevator.objects.filter(departure=departure, destination__node__contains='X').values()]
        return routes


def get_routes_of_end_building(end: str, elevator: bool) -> list:
    if not exist_node(end):
        return []
    destination = Node.objects.get(node=end)
    if elevator:
        if not ResultWithElevator.objects.filter(destination=destination).exists():
            print(NonExistentRoute)
            return []
        routes = [{'distance': result['distance'], 'route': result['route'].split(',')} for result in
                  ResultWithElevator.objects.filter(departure__node__contains='X', destination=destination).values()]
        return routes
    if not elevator:
        if not ResultWithoutElevator.objects.filter(destination=destination).exists():
            print(NonExistentRoute)
            return []
        routes = [{'distance': result['distance'], 'route': result['route'].split(',')} for result in
                  ResultWithoutElevator.objects.filter(departure__node__contains='X', destination=destination).values()]
        return routes


def exist_node(node: str) -> bool:
    if Node.objects.filter(node=node).exists():
        return True
    print(NonExistentNode, node)
    return False


def exist_route(start: str, end: str, elevator: bool) -> bool:
    if not exist_node(start):
        return False

    if not exist_node(end):
        return False
    departure = Node.objects.get(node=start)
    destination = Node.objects.get(node=end)
    if elevator:
        return ResultWithElevator.objects.filter(departure=departure, destination=destination).exists()
    if not elevator:
        return ResultWithoutElevator.objects.filter(departure=departure, destination=destination).exists()

from django.test import TestCase

from .models import Node, ResultWithElevator, ResultWithoutElevator, Coordinate
from .models import save


# Create your tests here.
class ModelNodeTest(TestCase):
    def setUp(self) -> None:
        # Given
        self.test_node = Node(node='TestNode-1-1')

    def test_create_node(self):
        # Then
        self.assertEquals(self.test_node.node, 'TestNode-1-1')

    def test_save_node(self):
        # When
        self.test_node.save()
        retrieved_node = Node.objects.get(pk=self.test_node.pk)

        # Then
        self.assertEquals(self.test_node, retrieved_node)


class ModelResultWithElevatorTest(TestCase):

    def test_create_result_with_elevator(self):
        # When
        test_node1 = Node(node="TestNode-1-1")
        test_node2 = Node(node="TestNode-1-2")
        test_node1.save()
        test_node2.save()
        created_result = ResultWithElevator(departure=test_node1, destination=test_node2,
                                            distance=10, route="TestRoute")

        # Then
        self.assertEquals(created_result.departure, test_node1)
        self.assertEquals(created_result.destination, test_node2)
        self.assertEquals(created_result.distance, 10)
        self.assertEquals(created_result.route, "TestRoute")

    def test_save_result_with_elevator(self):
        # When
        test_node1 = Node(node="TestNode-1-1")
        test_node2 = Node(node="TestNode-1-2")
        test_node1.save()
        test_node2.save()
        saved_result = ResultWithElevator(departure=test_node1, destination=test_node2,
                                          distance=10, route="TestRoute")
        saved_result.save()

        # Then
        self.assertEquals(saved_result, ResultWithElevator.objects.get(departure=test_node1,
                                                                       destination=test_node2))

    def test_primary_key_test(self):
        # When
        test_node1 = Node(node="TestNode-1-1")
        test_node2 = Node(node="TestNode-1-2")
        test_node1.save()
        test_node2.save()
        result1 = ResultWithElevator(departure=test_node1, destination=test_node2,
                                     distance=10, route="TestRoute1")
        result2 = ResultWithElevator(departure=test_node2, destination=test_node2,
                                     distance=20, route="TestRoute2")

        result1.save()
        result2.save()

        # Then
        self.assertEquals(result1, ResultWithElevator.objects.get(departure_id=result1.departure,
                                                                  destination_id=result1.destination))

        self.assertEquals(result2, ResultWithElevator.objects.get(departure_id=result2.departure,
                                                                  destination_id=result2.destination))


class ModelResultWithoutElevatorTest(TestCase):
    def test_create_result_with_elevator(self):
        # When
        test_node1 = Node(node="TestNode-1-1")
        test_node2 = Node(node="TestNode-1-2")
        test_node1.save()
        test_node2.save()
        created_result = ResultWithoutElevator(departure=test_node1, destination=test_node2,
                                               distance=10, route="TestRoute")

        # Then
        self.assertEquals(created_result.departure, test_node1)
        self.assertEquals(created_result.destination, test_node2)
        self.assertEquals(created_result.distance, 10)
        self.assertEquals(created_result.route, "TestRoute")

    def test_save_result_without_elevator(self):
        # When
        test_node1 = Node(node="TestNode-1-1")
        test_node2 = Node(node="TestNode-1-2")
        test_node1.save()
        test_node2.save()
        saved_result = ResultWithoutElevator(departure=test_node1, destination=test_node2,
                                             distance=10, route="TestRoute")
        saved_result.save()

        # Then
        self.assertEquals(saved_result, ResultWithoutElevator.objects.get(departure=test_node1,
                                                                          destination=test_node2))

    def test_primary_key_test(self):
        # When
        test_node1 = Node(node="TestNode-1-1")
        test_node2 = Node(node="TestNode-1-2")
        test_node1.save()
        test_node2.save()
        result1 = ResultWithoutElevator(departure=test_node1, destination=test_node2,
                                        distance=10, route="TestRoute1")
        result2 = ResultWithoutElevator(departure=test_node2, destination=test_node2,
                                        distance=20, route="TestRoute2")

        result1.save()
        result2.save()

        # Then
        self.assertEquals(result1, ResultWithoutElevator.objects.get(departure_id=result1.departure,
                                                                     destination_id=result1.destination))

        self.assertEquals(result2, ResultWithoutElevator.objects.get(departure_id=result2.departure,
                                                                     destination_id=result2.destination))


class ModelCoordinateTest(TestCase):
    def test_create_coordinate(self):
        # Given
        create_node = Node(node='TestNode-1-1')
        x = 10
        y = 20

        # When
        coordinate = Coordinate(node=create_node, x=x, y=y)

        # Then
        self.assertEquals(coordinate.node, create_node)
        self.assertEquals(coordinate.x, x)
        self.assertEquals(coordinate.y, y)

    def test_save_coordinate(self):
        # Given
        create_node = Node(node='TestNode-1-1')
        create_node.save()
        saved_coordinate = Coordinate(node=create_node, x=10, y=20)

        # When
        saved_coordinate.save()

        # Then
        self.assertEquals(Coordinate.objects.get(node=create_node), saved_coordinate)


class ModelFunctionTest(TestCase):
    def test_save(self):
        # Given
        test_result = {
            ('TestNode-1-1', 'TestNode-1-2'): {'distance': 10, 'route': 'TestRoute1'},
            ('TestNode-1-3', 'TestNode-1-3'): {'distance': 20, 'route': 'TestRoute2'},
        }
        # When
        save(test_result, elevator=True)
        save(test_result, elevator=False)

        # Then
        for (departure, destination), value in test_result.items():
            departure = Node(node=departure)
            destination = Node(node=destination)
            distance = value['distance']
            route = value['route']

            departure.save()
            destination.save()

            compared_result_with_elevator = ResultWithElevator(departure=departure, destination=destination,
                                                               distance=distance, route=route)
            compared_result_without_elevator = ResultWithoutElevator(departure=departure, destination=destination,
                                                                     distance=distance, route=route)

            self.assertEquals(compared_result_with_elevator,
                              ResultWithElevator.objects.get(departure=departure, destination=destination))
            self.assertEquals(compared_result_without_elevator,
                              ResultWithoutElevator.objects.get(departure=departure, destination=destination))

    def test_get_route(self):
        # Given
        test_result = {
            ('TestNode-1-1', 'TestNode-1-2'): {'distance': 10, 'route': 'TestRoute1'},
            ('TestNode-1-3', 'TestNode-1-3'): {'distance': 20, 'route': 'TestRoute2'},
        }

        # When
        save(test_result, elevator=True)
        save(test_result, elevator=False)

        # Then
        for (departure, destination), value in test_result.items():
            departure = Node(node=departure)
            destination = Node(node=destination)
            distance = value['distance']
            route = value['route']

            departure.save()
            destination.save()



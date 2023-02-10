class Amenity:
    def __init__(self):
        self.__amenities = dict()
        self._cafe()
        self._convenience_store()
        self._restaurant()
        self._medical_room()
        self._reading_room()

    @property
    def amenities(self):
        return self.__amenities

    def _cafe(self):
        self.__amenities['cafe'] = []

    def _convenience_store(self):
        self.__amenities['convenience_store'] = []

    def _restaurant(self):
        self.__amenities['restaurant'] = []

    def _medical_room(self):
        self.__amenities['medical_room'] = []

    def _reading_room(self):
        self.__amenities['reading_room'] = []

class Coordinate:
    y = None
    x = None
    def __init__(self,latitude,longitude):
        self.y = float(latitude)
        self.x = float(longitude)
    def getLatitude(self):
        return self.y
    def getLongitude(self):
        return self.x

class MatcherChain:
    _next = None
    _search = None
    def _matches(self, subject):
        return self._search.lower() in subject.lower()
    def __init__(self, matching, nextHandler = None):
        super().__init__()
        self._search = matching
        self._next = nextHandler
    def _onMatch(self, subject):
        return self
    def _onNoMatch(self, subject):
        return None
    def match(self,subject):
        if self._matches(subject):
            return self._onMatch(subject)
        elif not self._next is None:
            return self._next.match(subject)
        else:
            return self._onNoMatch(subject)
    def matchAll(self,subject,matched = None):
        if matched is None: matched = list()
        if self._matches(subject):
            matched.append(self._onMatch(subject))
        if self._next is None:
            return matched
        return self._next.matchAll(subject,matched)

class City(Coordinate, MatcherChain):
    name = None
    def __init__(self,latitude,longitude,name,next=None):
        Coordinate.__init__(self,latitude,longitude)
        MatcherChain.__init__(self,name,next)
        self.name = str(name)
    def getName(self):
        return self.name

class CardinalDirection(MatcherChain):
    def _matches(self, subject):
        return subject.lower().endswith(self._search.lower())
    def directionmost(self, cityList):
        if len(cityList) <= 0:
            return None
        most = cityList[0]
        for city in cityList[1:]:
            if self.isGreater(city,most):
                most = city
        return most
    def isGreater(self, cityA, cityB):
        return False

class North(CardinalDirection):
    def __init__(self, nextHandler = None):
        super().__init__('norte',nextHandler)
    def isGreater(self, cityA, cityB):
        return cityA.getLatitude() > cityB.getLatitude()

class South(CardinalDirection):
    def __init__(self, nextHandler = None):
        super().__init__('sul',nextHandler)
    def isGreater(self, cityA, cityB):
        return cityA.getLatitude() < cityB.getLatitude()

class West(CardinalDirection):
    def __init__(self, nextHandler = None):
        super().__init__('oeste',nextHandler)
    def isGreater(self, cityA, cityB):
        return cityA.getLongitude() < cityB.getLongitude()

class East(CardinalDirection):
    def __init__(self, nextHandler = None):
        super().__init__('leste',nextHandler)
    def isGreater(self, cityA, cityB):
        return cityA.getLongitude() > cityB.getLongitude()

class FoobarCarSystem:
    currentLocation = None
    _cities = None
    _cardinalDirections = None
    def __init__(self, cityMatcher, currentLocation = None):
        super().__init__()
        self._cardinalDirections = North(South(West(East(None))))
        self.currentLocation = currentLocation
        self._cities = cityMatcher
    def updateCurrentLocation(self, currentLocation):
        self.currentLocation = currentLocation
    def search(self, query):
        locations = list()
        if not self._cities is None:
            locations = self._cities.matchAll(query)
        if not self.currentLocation is None:
            locations.append(self.currentLocation)
        cardinalDirection = self._cardinalDirections.match(query)
        if cardinalDirection is None:
            return None
        return cardinalDirection.directionmost(locations)

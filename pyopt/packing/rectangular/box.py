__author__ = 'Alex Baranov'
from copy import deepcopy
from json import JSONEncoder


class Box(object):
    """Represents the box element"""

    @staticmethod
    def from_json_dict(d):
        """
        Parses the box from the JSON dict
        """
        return Box(d['size'], bottom_left=d['polus'], name=d['name'], kind=d['kind'], weight=d['weight'])

    def __init__(self, size=(), bottom_left=(), name="", kind="solid", weight=None):
        """
        Constructor for box.
              +-------------+
             /             /|
            +-------------+ +
            |             |/
            +-------------+

        Arguments:
            - size: (tuple or list) the element linear sizes.
            - bottom_left:  (list) the coordinates to the button left corner of the element.
            - name: (string) the name of the box.
            - kind: (string) the type of the box.
        """
        super(Box, self).__init__()
        self.size = size
        self.name = name
        self.kind = kind
        self.weight = weight or 0

        if bottom_left == ():
            bottom_left = tuple(0 for _ in xrange(len(size)))

        if len(bottom_left) != len(size):
            raise ValueError("The length of the 'size' argument should be equal to the size of 'bottom_left' argument")
        self.polus = bottom_left

    @property
    def diagonal_polus(self):
        """
        The top left cornet of the rectangle
        """
        return list(self.polus[i] + self.size[i] for i in xrange(len(self.size)))

    @property
    def center(self):
        """
        Get the center position of the box.
        """
        return list(self.polus[i] + self.size[i] / 2.0 for i in xrange(len(self.size)))

    def get_area(self):
        """
        Calculates the area of the rectangle
        """

        return reduce(lambda x, y: x * y, self.size)

    def find_phi_function_value(self, p):
        """
        Gets the Phi-function value that characterise the placement of two box's
        If phi value is greater than 0: objects are NOT intersecting.
        If phi = 0: objects are touching.
        If fi less than 0: object are intersecting.

        Arguments:
            - p : another box.
        """

        n = len(self.size)
        if len(p.size) != n:
            raise ValueError("Unable to compare box's with different dimensions")

        values = []
        for i in xrange(n):
            values.append(p.polus[i] - self.polus[i] - self.size[i])
            values.append(-p.polus[i] + self.polus[i] - p.size[i])

        return max(values)

    def touches(self, other):
        """
        Checks whether current box touches the another one.
        """

        return self.find_phi_function_value(other) == 0

    def intersects(self, other):
        """
        Checks whether two box's are intersecting.
        """
        phi = self.find_phi_function_value(other)
        return phi < 0

    def includes_point(self, p):
        """
        Checks whether the provided point is within the box.

        Arguments:
            p - the list of point coordinates.
        """
        return all((p[i] - x >= 0 for i, x in enumerate(self.polus))) and all(
            (x - p[i] >= 0 for i, x in enumerate(self.diagonal_polus)))

    def includes(self, other):
        """
        Checks whether the current box includes the another one.
        """
        return self.includes_point(other.polus) and self.includes_point(other.diagonal_polus)

    def can_accept(self, other):
        """
        Checks whether the box can accept the another one.

        Arguments:
            - other: the another box

        Returns:
            - True or False.
        """

        return all((value - other.size[index]) >= 0 for index, value in enumerate(self.size))

    def find_free_containers(self, other):
        """
        Gets the list of containers that can be received by placing
        another box into current.

        +-------------------+
        |   a               |
        |                   |
        +-------+           |
        | other |      b    |
        +-------+-----------+


        Arguments:
            - other : the placed box. The polus should be defined.

        Returns:
            - the list of container received.
        """

        assert isinstance(other, Box)
        result = []

        # TODO Rework this to be more pythonic
        n = len(self.size)
        for i in range(n):
            if other.diagonal_polus[i] < self.diagonal_polus[i]:
                # create free container
                polus = []
                size = []
                for j in range(n):
                    if i != j:
                        polus.append(self.polus[j])
                    else:
                        polus.append(other.diagonal_polus[j])

                    size.append(self.diagonal_polus[j] - polus[j])

                result.append(Box(tuple(size), tuple(polus)))
            if other.polus[i] > self.polus[i]:
                polus = self.polus[:]
                size = self.size[:i] + (other.polus[i], ) + self.size[i + 1:]

                result.append(Box(size, polus))

        return result

    def is_blocked(self, other, axes=()):
        """
        Checks whether the current box is blocked the another one.

        By default checks whether the box is blocked by another one by +X axis.

        Arguments:
            other: the other box.
            axes: the tuple of axes to check. For example (1,0,0) checks that block by X axis for 3d case.

        Returns:
            - boolean value.
        """

        if len(other.size) != len(self.size):
            raise ValueError("Boxes sizes should have the same lengths")

        if not axes:
            axes = [0] * len(self.size)
            axes[0] = 1

        checks = []

        c = deepcopy(self)
        for i, a in enumerate(axes):
            # create a copy of the current box.
            c.size = list(c.size)
            c.size[i] += (other.polus[i] + other.size[i]) * a
            checks.append(other.intersects(c))

        return any(checks)

    def is_basis_for(self, other, axes=()):
        """
        Check if current box is basis for another box.
        Be default check is performed by Y axis.

        Example: self is basis for other

           +-------+
           | other |
        +--+-------+--------+
        |                   |
        |       self        |
        |                   |
        |                   |
        +-------------------+
        """
        if len(other.size) != len(self.size):
            raise ValueError("Boxes sizes should have the same lengths")

        if not axes:
            axes = [0] * len(self.size)
            axes[1] = 1

        if not self.touches(other):
            return False

        c = deepcopy(self)
        for i, a in enumerate(axes):
            c.size = list(c.size)
            c.size[i] += (other.polus[i] + other.size[i]) * a

        return c.includes(other)

    def __str__(self):
        """
        String representation of the object.
        """
        return "Box: Name '{}'; Size: '{}'; Polus: '{};".format(self.name, self.size, self.polus)

    def __eq__(self, other):
        """
        Checks whether the current container is equal to other.
        Position is ignored.
        """

        return self.size == other.size and self.name == other.name and \
               self.kind == other.kind

    def __lt__(self, other):
        """
        Compares the areas of boxes
        """
        self.get_area() < other.get_area()

    def __le__(self, other):
        """
        Compares the areas of boxes
        """
        self.get_area() <= other.get_area()

    def __gt__(self, other):
        """
        Compares the areas of boxes
        """
        self.get_area() > other.get_area()

    def __ge__(self, other):
        """
        Compares the areas of boxes
        """
        self.get_area() >= other.get_area()

    def __ne__(self, other):
        """
        Checks that currents box is not equal to another one.
        """
        return not self == other

    def clone(self):
        """
        Returns the deep copy of the box.
        """
        return deepcopy(self)


class BoxJsonEncoder(JSONEncoder):
    """
    Serializes box into json format.
    """

    def default(self, obj):
        if not isinstance(obj, Box):
            return super(BoxJsonEncoder, self).default(obj)

        return dict(obj.__dict__, **{'__type__': 'Box'})

__author__ = "Alex Baranov"


class CombinatorialSet(object):
    """
    Contains the base definition of the set. Defines methods that should be impelemented for the specific sets.
    """

    def __init__(self, s=()):
        self.generation_elements = sorted(s)

    def __iter__(self):
        raise NotImplementedError

    def find_nearest_set_point(self, p):
        """
        Gets the set point that is the closest one to the provided point 'p'.
        """
        raise NotImplementedError

    def find_min_of_linear_function(self, coefs):
        """
        Gets the minimum of the linear function on a given set.
        """
        raise NotImplementedError

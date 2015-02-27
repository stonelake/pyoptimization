__author__ = "Alex Baranov"

import itertools as it
from combinatorial_set import CombinatorialSet


class PermutationSet(CombinatorialSet):
    """
    Describes the set of permutations
    """
    def __init__(self, s=()):
        super(PermutationSet, self).__init__(s)

    def __iter__(self):
        for x in it.permutations(self.generation_elements):
            yield x

    def find_min_of_linear_function(self, coefs):
        """
        Gets the minimum of the linear function on the given set.

        Parameters:
         - coefs - the coefficients (c_i) of the linear function of type F(x) = sum(c_i*x_i)
        """
        # getting the func coefs with the initial indexes
        dict_coefs = dict(enumerate(coefs))

        # getting indexes. In this case we know which element of set correspond to the given element of the coefs
        keys = sorted(dict_coefs, key=dict_coefs.get, reverse=True)

        # copy generation elements
        res = list(self.generation_elements)

        # take each set elements according the keys.
        for i, j in enumerate(keys):
            res[j] = self.generation_elements[i]

        return res

    def find_nearest_set_point(self, p):
        """
        Gets the nearest set point related to the given point 'p'

        Parameters:
         - p - some point in the space
        """
        # converting point
        c = [-2 * x for x in p]
        return self.find_min_of_linear_function(c)

if __name__ == '__main__':
    p = PermutationSet((1, 2, 3, 4))
    print p.generation_elements

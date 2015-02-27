___author___ = "Olga Titova"

import itertools as it
from branchandbound import BranchAndBound
from combinatorial_set import CombinatorialSet


class CyclePermutationSet(CombinatorialSet):
    """
    Describes the set of permutations
    """
    def __init__(self, s=()):
        super(CyclePermutationSet, self).__init__(s)

    def __iter__(self):
        cp = [[4, 1, 2, 3], [4, 1, 3, 2], [2, 4, 1, 3], [3, 1, 4, 2], [2, 3, 4, 1], [3, 4, 2, 1]]
        #cp = [[2, 3, 1], [3, 1, 2]]
        for c in cp:
            yield  c

    def find_min_of_linear_function(self, coefs):
        """
        Gets the minimum of the linear function on the given set.

        Parameters:
         - coefs - the coefficients (c_i) of the linear function of type F(x) = sum(c_i*x_i)
        """

        bb = BranchAndBound(self.generation_elements, coefs)
        return bb.findcyclemin(self.generation_elements).Adress[1:]

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
    p = CyclePermutationSet((1, 2, 3, 4))
    print p.find_min_of_linear_function([-0.09, -0.06, -0.03, -0.05])

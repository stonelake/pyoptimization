from pyopt.discrete.permutations import PermutationSet
from pyopt.discrete.randomsearch import (find_minimum_with_exhaustive_search,
                                         find_minimum)

from pyopt.packing.rectangular.rpacker import RPacker

s = [[1, -2, 3, 0], [-4, 1, 1, 2]]

func = (-1, 1, 2)
pset = PermutationSet((1, 2, 3))

point, func_value = find_minimum_with_exhaustive_search(func, s, pset)
print "Point and min fuc value found using exhaustive search: ", (point, func_value)

point2, func_value2 = find_minimum(func, s, pset, quiet=False)
print "Point and min fuc value found using random search: ", (point2, func_value2)

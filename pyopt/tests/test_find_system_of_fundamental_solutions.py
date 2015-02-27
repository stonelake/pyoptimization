__author__ = 'Alex Baranov'


import unittest
from time import *
import numpy as np

from ..discrete.inequalities import chernikov as c


class TestFind_system_of_fundamental_solutions(unittest.TestCase):
    def _test_pulp(self):
        import pulp as p
        prob = p.LpProblem("The Whiskas Problem", p.LpMinimize)
        elapsed = -clock()

        # creating variables
        x1 = p.LpVariable("ChickenPercent", 0, None, p.LpInteger)
        x2 = p.LpVariable("BeefPercent", 0, None, p.LpInteger)

        # goal function
        a = 0.013 * x1 + 0.008 * x2
        prob += 0.013 * x1 + 0.008 * x2

        # constraints
        prob += x1 + x2 == 100, "PercentagesSum"
        prob += 0.100 * x1 + 0.200 * x2 >= 8.0, "ProteinRequirement"
        prob += 0.080 * x1 + 0.100 * x2 >= 6.0, "FatRequirement"
        prob += 0.001 * x1 + 0.005 * x2 <= 2.0, "FibreRequirement"
        prob += 0.002 * x1 + 0.005 * x2 <= 0.4, "SaltRequirement"

        # solution
        prob.writeLP("WhiskasModel.lp")
        prob.solve(p.GLPK(msg=0))

        print "Status:", p.LpStatus[prob.status]
        for v in prob.variables():
            print v.name, "=", v.varValue

        print "Total Cost of Ingredients per can = ", p.value(prob.objective)
        elapsed  = +clock()
        print "Solution time = ", prob.solutionTime
        print "Solution time2 = ", elapsed

    def test_find_system_of_fundamental_solutions(self):
        """
        Verify simple scenario for Chernikov method
        """
        sys = [[-5,-5,6,-8,-10,0],[0,-5,3,1,0,-10]]
        result1 = c.find_sfs_of_equation_system(sys)
        expected1 = np.array([[ 12.,   0.,  10.,   0.,   0.,   3.],
                     [  0.,   0.,   8.,   6.,   0.,   3.],
                     [  0.,   0.,  10.,   0.,   6.,   3.],
                     [  3.,   3.,   5.,   0.,   0.,   0.],
                     [  0.,   2.,  3.,   1.,   0.,   0.],
                     [  0.,   6.,  10.,   0.,   3.,   0.]])
        self.assertTrue(np.array_equal(expected1,np.array(result1)))

        sys2 = [[1,-1,3,-8,5],[-1,2,-1,1,-1],[2,-1,-2,1,0],[-3,1,-1,6,-3],[1,1,-3,2,-1]]
        result2 = c.find_sfs_of_even_inequalities_system(sys2)
        expected2 = np.array([[ 13.,   0.,  17.,   8.,   0.],
                              [ 15.,  11.,  12.,   5.,   0.],
                              [  5.,   0.,   9.,   4.,   0.],
                              [  5.,   5.,   8.,   3.,   0.],
                              [  2.,   0.,   3.,   2.,   1.],
                              [ 11.,   0.,  15.,   8.,   0.],
                              [ 13.,   9.,  12.,   7.,   0.],
                              [  1.,   1.,   1.,   1.,   1.]])
        self.assertTrue(np.array_equal(expected2, np.array(result2)))

if __name__ == '__main__':
    unittest.main()

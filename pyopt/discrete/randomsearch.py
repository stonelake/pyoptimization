__author__ = "Alex Baranov"

from inequalities import chernikov as c
from permutations import *
import numpy as np


def find_minimum(goal_func,
                 constraints_system,
                 combinatorial_set,
                 add_constraints=True,
                 series_count=3,
                 experiments_per_series=5,
                 quiet=True):
    """
    Gets the minimum of the linear function with linear constraints
    on the combinatorial set

    Returns:
        - (point and function value)
    """

    # define function to calculate goal function value
    f = lambda x: sum(i * j for i, j in zip(goal_func, x))

    # copying the constraints system to modify it then
    copied_system = list(constraints_system)

    if add_constraints:
        if not quiet:
            print "Addding additional constraints to the constraints system"
        copied_system = add_additional_constraints(copied_system, combinatorial_set.generation_elements)

    if not quiet:
        print "Constraints system is: \n", np.array(copied_system)

    solver = c.InequalitiesSolver()
    best_func_value = None
    best_point = None
    last_system_index = len(copied_system)
    const_was_inserted = False

    # starting series of experiments
    for series_number in xrange(series_count):
        if not quiet:
            print "---> Starting series #", series_number

        # store the valid points in the dict
        experiment_valid_points = dict()
        for experiment_number in xrange(experiments_per_series):
            if not quiet:
                print "Starting experiment #", experiment_number

            # getting some solution of the system
            s = solver.get_solution(copied_system)
            if not quiet:
                print "Generated new point within the search area: ", s

            # get the nearest point of the set
            nearest_set_point = combinatorial_set.find_nearest_set_point(s)
            if not quiet:
                print "The nearest combinatorial set point is: ", nearest_set_point

            # check whether the set point is valid
            if is_solution(copied_system, nearest_set_point):
                func_value = f(nearest_set_point)
                experiment_valid_points[func_value] = nearest_set_point
                if not quiet:
                    print "Found point is valid. Goal function value in this point is: ", func_value
            else:
                if not quiet:
                    print "The nearest set point is not valid"

        # save this point
        if len(experiment_valid_points):
            current_min = min(experiment_valid_points)
            if best_func_value is None or current_min < best_func_value:
                best_func_value = min(experiment_valid_points)
                best_point = experiment_valid_points[best_func_value]

            if not quiet:
                print "Current best point {0} with function value = {1}".format(best_point, best_func_value)

            # add the aditional constraint to shrink the search area.
            if not quiet:
                print "Added additional constraints: {0} <= {1}".format(goal_func, best_func_value)

            if not const_was_inserted:
                copied_system.append(goal_func + (-1 * best_func_value,))
            else:
                copied_system.insert(last_system_index, goal_func + (-1 * best_func_value,))

    return best_point, best_func_value


def add_additional_constraints(system, coefs, add_less_then_zero=False, add_simplex=True):
    """
    Adds additional constraints to the constraints system.
    First adds the constraints of type: -x_i <= 0
    If add_simplex parameter is True than add also constraints to bounds all the elements of the
    combinatorial set with the simplex.

    Arguments:
        system -- the matrix that represents the constraint system
        coefs -- the array of coefficients that will be used to add new constraints
        add_less_then_zero -- specifies whether the constraints of type: -x_i <= 0 should be added (default - True)
        add_simplex -- specifies whether the simplex constraints should be added (default - True)
    """

    constraints_system = np.array(system)
    constraint_coefs = np.array(coefs)
    var_count = constraints_system.shape[1]

    if add_less_then_zero:
        # add conditional constraints that all variables are less or equal than zero
        left_part = -1 * np.eye(var_count - 1)
        right_part = np.zeros([var_count - 1, 1])
        positive_variables_consts = np.hstack((left_part, right_part))
        constraints_system = np.vstack((constraints_system, positive_variables_consts))

    if add_simplex:
        left_part = np.eye(var_count - 1)
        min = constraint_coefs.min()
        sum = constraint_coefs.sum()
        right_part1 = min * np.ones([var_count - 1, 1])

        # first add constraints of type: x_i >= min
        type1 = np.hstack((-1 * left_part, right_part1))

        # first add constraints of type: sum(x_i) <= sum
        type2 = np.hstack((np.ones(var_count - 1), -1*sum))
        constraints_system = np.vstack((constraints_system, type1))
        constraints_system = np.vstack((constraints_system, type2))

    return constraints_system.tolist()


def find_minimum_with_exhaustive_search(goal_func,
                                        system,
                                        combinatorial_set):
    """
    Gets the solution by iterating all the elements in the set

    Retruns pair of combinatorial element and minimal function value
    """

    #calcualte goal functions for all the elements
    valid_values = map(lambda e: (e, sum(i * j for i, j in zip(goal_func, e))) if is_solution(system, e) else None, combinatorial_set)

    # remove all the None
    valid_values = filter(lambda x: x != None, valid_values)

    # get minimal value
    return min(valid_values, key=lambda x: x[1])


def is_solution(system, point):
    """
    Checks whether the point is the solution for a given constraints system.
    """
    a = np.array(system)

    # get the left part
    left = a[:, :-1] * point
    left = sum(left.T)

    # get the right part
    right = (-1) * a[:, -1]
    return np.all(left <= right)


if __name__ == '__main__':
    s = [[1, -2, 3, 0], [-4, 1, 1, 2]]
    func = (-1, 1, 2)
    pset = PermutationSet((1, 2, 3))
    point, func_value = find_minimum_with_exhaustive_search(func, s, pset)
    print "Point and min fuc value found using exhaustive search: ", (point, func_value)

    point2, func_value2 = find_minimum(func, s, pset, quiet=False)
    print "Point and min fuc value found using random search: ", (point2, func_value2)

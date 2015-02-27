__author__ = 'Alex Baranov'

import numpy as np
import itertools as iter

__PRINT_DEBUG = False


class InequalitiesSolver(object):
    last_system = None
    last_found_fundamental_system = None
    min_random = 1
    max_random = 1000

    def find_foundamental_system_of_solution(self, system):
        """
        Searches the fundamental systems of non-nagative solutions for the ineqalities system

        Parameters

         - system: matrix of ineqailities coefs (ax + by + cz + d .... <= 0)
        """
        self.last_system = np.array(system)
        self.last_found_fundamental_system = find_sfs_of_even_inequalities_system(system)
        return self.last_found_fundamental_system

    def get_solution(self, system, p=None):
        """
        Gets the solution that agrees with the system.
        """
        npsystem = np.array(system)
        if not np.array_equal(npsystem, self.last_system):
            # need to recalcualate the fundamental system
            self.find_foundamental_system_of_solution(system)

        # numbers of rows in the fundamental system
        n = self.last_found_fundamental_system.shape[0]

        if (self.last_found_fundamental_system == 0).all():
            return [0] * (npsystem.shape[1] - 1)

        # use provided or generate random coefficients
        if p is None:
            # generate random coefs
            p = np.random.random_integers(self.min_random, self.max_random, (n, 1))
            while(p <= 0).all():
                p = np.random.random_integers(self.min_random, self.max_random, (n, 1))

        # getting random solution
        mult = p * self.last_found_fundamental_system
        b = sum(mult[:, :-1]) / sum(mult[:, -1])
        return b


def add_additional_constraints(constraints_system, constraint_coefs, add_less_then_zero=True, add_simplex=True):
    """
    Adds additional constraints to the constraints system.
    First adds the constraints of type: -x_i <= 0
    If add_simplex parameter is True than add also constraints to bounds all the elements of the
    combinatorial set with the simplex.

    Keyword arguments:
        constraints_system -- the matrix that represents the constraint system
        constraint_coefs -- the array of coefficients that will be used to add new constraints
        add_less_then_zero -- specifies whether the constraints of type: -x_i <= 0 should be added (default - True)
        add_simplex -- specifies whether the simplex constraints should be added (default - True)
    """

    var_count = constraints_system.shape[1]

    if add_less_then_zero:
        # add conditional constraints that all variables are less or equal than zero
        left_part = -1 * np.eye(var_count - 1)
        right_part = np.zeros([var_count - 1, 1])
        positive_variables_consts = np.hstack((left_part, right_part))
        constraints_system = np.vstack((constraints_system, positive_variables_consts))

    if add_simplex:
        left_part = np.eye(var_count - 1)
        min = -1 * constraint_coefs.min()
        sum = constraint_coefs.sum()
        right_part1 = min * np.ones([var_count - 1, 1])
        right_part2 = sum * np.ones([var_count - 1, 1])

        # first add constraints of type: x_i >= min
        type1 = np.hstack((-1 * left_part, right_part1))

        # first add constraints of type: x_i <= sum
        type2 = np.hstack((left_part, right_part2))
        constraints_system = np.vstack((constraints_system, type1))
        constraints_system = np.vstack((constraints_system, type2))

    return constraints_system


def find_sfs_of_equation_system(system):
    """
    Calculates the system of the fundamental solutions using the Chernikov method for the linear system of equations

    Keyword arguments:
        system -- constraints matrix
    """
    constraints_system = np.array(system)

    # First build initial T1 and T2 matrices
    # T1 is a matrix with ones on the main diagonal
    T1 = [np.eye(constraints_system.shape[1])]

    # T2 is a transposed matrix of the initial matrix formed by the constraints system
    T2 = [constraints_system.transpose().copy()]

    current_index = 0
    next_index = 1

    while np.any(T2[current_index] != 0):
        # No choose the main column
        main_column = __get_main_column_index_simple(T2[current_index])
        if __PRINT_DEBUG:
            print "----> Main colum is ", main_column
        # Copy to a new T1 and T2 rows from T1 and T2 that are intersected
        # with the main column by zero elements
        T1.append(np.zeros((0, T1[current_index].shape[1]), dtype=T1[current_index].dtype))
        T2.append(np.zeros((0, T2[current_index].shape[1]), dtype=T2[current_index].dtype))
        rows_to_modify = []

        for index, row in enumerate(T2[current_index]):
            if (T2[current_index][index, main_column] == 0):
                #copy this row into a new T
                T1[next_index] = np.vstack((T1[next_index], T1[current_index][index]))
                T2[next_index] = np.vstack((T2[next_index], row))
                if __PRINT_DEBUG:
                    print "Copying row to the new table: ", index
            else:
                rows_to_modify.append(index)

        # Not find all pairs from rows_to_modify where the sign on main column are different
        pairs = list(iter.combinations(rows_to_modify, 2))
        valid_pairs = []

        for i, j in pairs:
            main_i = T2[current_index][i, main_column]
            main_j = T2[current_index][j, main_column]

            if ((main_i != 0) & (main_j != 0) & (cmp(main_i, 0) != cmp(main_j, 0))):
                # also need to check that there are zero columns in the T1 for given pair
                columns = np.where((T1[current_index][i] == 0) & (T1[current_index][j] == 0))[0]

                # check whether there is another row (except i,j) in T1 which intersect all the columns with zereos
                tmp = np.delete(T1[current_index][:, columns], [i, j], 0)

                if ((np.where(np.all(tmp == 0, axis=1))[0].size == 0) or (len(pairs) == 0)):
                    valid_pairs.append([i, j])

        for i, j in valid_pairs:
            if __PRINT_DEBUG:
                print "Checking row pair: ", (i, j)
            #build linear combinations for valid pairs to have zeros on main column
            coef_j = abs(T2[current_index][j][main_column])
            coef_i = abs(T2[current_index][i][main_column])
            coefs = np.array([coef_i, coef_j])

            # trying to reduce coefs
            min = coefs.min()
            if (np.all(coefs % min == 0)):
                coefs = coefs / min

            new_row_T1 = T1[current_index][i] * coefs[1] + T1[current_index][j] * coefs[0]
            new_row_T2 = T2[current_index][i] * coefs[1] + T2[current_index][j] * coefs[0]
            T1[next_index] = np.vstack((T1[next_index], new_row_T1))
            T2[next_index] = np.vstack((T2[next_index], new_row_T2))

        current_index = current_index + 1
        next_index = next_index + 1

    if (T1[-1].size == 0):
        # return zero solution
        result = T1[-2]
        result.fill(0)
    else:
        result = T1[-1]

    reduce_table(result)
    if __PRINT_DEBUG:
        __print_T(T1, T2)

    return result


def find_sfs_of_even_inequalities_system(system):
    """
    Calculates the system of the fundamental solutions using the Chernikov method for the even linear system of inequalities

    Keyword arguments:
        system -- constraints matrix
    """

    # casting to array.
    constraints_system = np.array(system)

    # First build initial T1 and T2 matrices
    # T1 is a matrix with ones on the main diagonal
    T1 = [np.eye(constraints_system.shape[1])]

    # T2 is a transposed matrix of the initial matrix formed by the constraints system
    T2 = [constraints_system.transpose().copy()]

    current_index = 0
    next_index = 1

    # stores all the previous main columns
    saved_main_column = []
    saved_main_column_indexes = []

    while np.any(T2[current_index] > 0):
        # replace negative all negative columns with zero
        for index, column in enumerate(T2[current_index].T):
            if (column < 0).all() and not(index in saved_main_column_indexes):
                T2[current_index][:, index] = 0

        main_column = __get_positive_main_column_index(T2[current_index])
        if __PRINT_DEBUG:
            print "Main column is: ", main_column

        # Copy to a new T1 and T2 rows from T1 and T2 that are intersected
        # with the main column by negative (<=) elements
        T1.append(np.zeros((0, T1[current_index].shape[1]), dtype=T1[current_index].dtype))
        T2.append(np.zeros((0, T2[current_index].shape[1]), dtype=T2[current_index].dtype))

        for index, row in enumerate(T2[current_index]):
            if (T2[current_index][index, main_column] <= 0):
                #copy this row into a new T
                T1[next_index] = np.vstack((T1[next_index], T1[current_index][index]))
                T2[next_index] = np.vstack((T2[next_index], row))

        # find all 'valid pairs'
        pairs = list(iter.combinations(range(T2[current_index].shape[0]), 2))
        if __PRINT_DEBUG:
            print "All row pairs to check: ", pairs

        # forming the temporary T1 table which includes the saved main rows
        temp_T1 = __build_adjusted_T1(T1[current_index], T2[current_index], saved_main_column_indexes)

        for i, j in pairs:
            main_i = T2[current_index][i, main_column]
            main_j = T2[current_index][j, main_column]
            valid_pairs = []
            if ((main_i != 0) & (main_j != 0) & (cmp(main_i, 0) != cmp(main_j, 0))):
                if (temp_T1.shape[0] <= 2):
                    valid_pairs.append([i, j])
                else:
                    # also need to check that there are zero columns in the T1 for given pair
                    columns = np.where((temp_T1[i] == 0) & (temp_T1[j] == 0))[0]

                    # check whether there is another row (except i,j) in T1 which intersect all the columns with zereos
                    tmp = np.delete(temp_T1[:, columns], [i, j], 0)
                    if np.where(np.all(tmp == 0, axis=1))[0].size == 0 and tmp.shape[1] > 1:
                        valid_pairs.append([i, j])

                for i, j in valid_pairs:
                    if __PRINT_DEBUG:
                        print "Performing calcualtions for pair: ", (i, j)
                    #build linear combinations for valid pairs to have zeros on main column
                    coef_j = abs(T2[current_index][j][main_column])
                    coef_i = abs(T2[current_index][i][main_column])
                    coefs = np.array([coef_i, coef_j])

                    # trying to reduce coefs
                    d = gcd(coef_i, coef_j)
                    coefs = coefs / d

                    new_row_T1 = T1[current_index][i] * coefs[1] + T1[current_index][j] * coefs[0]
                    new_row_T2 = T2[current_index][i] * coefs[1] + T2[current_index][j] * coefs[0]
                    T1[next_index] = np.vstack((T1[next_index], new_row_T1))
                    T2[next_index] = np.vstack((T2[next_index], new_row_T2))

        # replace by -1 all the non-zero element of the main column. also replace all the saved main
        for column_index in saved_main_column_indexes + [main_column]:
            T2[next_index][np.where(T2[next_index][:, column_index] != 0), column_index] = -1

        if  np.all((T2[next_index] > 0), axis=0).any():
            # some column in the T2 is strickly positive"
            # in this case we have zero solution
            T1[next_index] = np.zeros_like(T1[next_index])
            break

        # saving the main column
        c = T2[next_index][:, main_column].copy()
        c = c.reshape(c.shape[0], 1)
        saved_main_column.append(c)
        saved_main_column_indexes.append(main_column)

        # going to the next tables
        current_index = current_index + 1
        next_index = next_index + 1

    # searching GCD
    reduce_table(T1[-1])

    if __PRINT_DEBUG:
        __print_T(T1, T2)
    # return the last left table
    return T1[-1]


def reduce_table(T1):
    for index, value in enumerate(T1):
        d = reduce(gcd, value)
        if (d != 0):
            T1[index] /= d


def __get_main_column_index_simple(T2):
    for index, value in enumerate(T2.T):
        if (value != 0).any():
            return index
    return -1


def __get_positive_main_column_index(T2):
    for index, value in enumerate(T2.T):
        if (value > 0).any():
            return index
    return -1


def __print_T(T1, T2):
    """
    Prints the T1 and T2 tables.
    """
    np.set_printoptions(precision=3, suppress=True, threshold=np.nan)
    for t_index in xrange(len(T1)):
        print "Table T[{0}]:".format(t_index)

        result = np.zeros((T1[t_index].shape[0], 0), dtype=T1[t_index].dtype)
        result = np.hstack((result, T1[t_index]))
        delimiter = np.zeros((T1[t_index].shape[0], 1))
        delimiter.fill(np.nan)
        result = np.hstack((result, delimiter))
        result = np.hstack((result, T2[t_index]))

        print result
        print "-" * (T1[t_index].shape[1] + T2[t_index].shape[1])


def __build_adjusted_T1(T1, T2, saved_columns_indexes):
    temp_T1 = T1.copy()
    if len(saved_columns_indexes) <= 0:
        return temp_T1

    # getting the actual saved columns from the T2
    saved_columns = T2[:, saved_columns_indexes]
    temp_T1 = np.hstack((temp_T1, saved_columns))
    return temp_T1


def gcd(a, b):
    return a if b == 0 else gcd(b, a % b)


def lcm(a, b):
    return a * b / gcd(a, b)


if __name__ == '__main__':
    a = np.float_([[-1, 0, 0, 1],
                   [0, -1, 0, 1],
                   [0, 0, -1, 1],
                   [1, 1, 1, -6]])
    #a = [[1,1,1,-1],
    #     [-1,1,-1,1],
    #     [-2, 1, -1,-2],
    #    [1,2,-2,1],
    #    [-2,-2,1,-2]]
    s = InequalitiesSolver()
    b = s.get_solution(a)
    b0 = s.get_solution(a)
    b1 = s.get_solution(a)
    b2 = s.get_solution(a)
    print b
    print b1
    print b2

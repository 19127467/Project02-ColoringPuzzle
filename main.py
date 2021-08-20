from CNF import *
from typing import List, Set, Dict, Tuple, Optional, Any
from time import perf_counter
from pysat.solvers import Glucose3

#testing 
#Function for solving puzzle by using Pysat library:
def Pysat_ver(m: int, n: int, mat: List[int]) -> Tuple[List[int], float]:
    clauses, result = [], []

    time_start = perf_counter()
    clauses = final_CNF_clauses(mat, m, n)

    g = Glucose3()
    for it in clauses:
        g.add_clause([int(k) for k in it])
    print(g.solve())
    model = g.get_model()
    print(model, '\n')

    """ printMatrix(mat)
    print('')
    for i in range(m):
        for j in range(n):
            if i*n+j+1 in model:
                print('G', end=' ')
            else:
                print('_', end=' ')
        print('') """
    
    for i in range(m):
        temp = []
        for j in range(n):
            if (i*n+j+1 in model):
                temp.append(1)
            else:
                temp.append(0)
        result.append(temp)

    time_stop = perf_counter()


    return result, time_stop - time_start


#Function for solving puzzle by using the Backtracking algorithm:
def Backtracking_ver(m: int, n: int, mat: List[int]) -> Tuple[List[int], float]:
    start = perf_counter()
    #prepare needed variables:
    result = []
    cell_with_unnega_value = get_cells_with_unnega_val(m, n, mat)

    for _ in range(m):
        temp = []
        for _ in range(n):
            temp.append(0)
        result.append(temp)

    #Backtracking:
    if (not Solve_cell_backtrack(0, cell_with_unnega_value, m, n, result, mat)):
        for row in range(m):
            for col in range(n):
                result[row][col] = -1

    end = perf_counter()
    
    return result, end - start


#Function for solving puzzle by using the Brute Force algorithm:
def Brute_Force_ver(m: int, n: int, mat: List[int]) -> Tuple[List[int], float]:
    start = perf_counter()
    #prepare needed variables:
    result = []
    for _ in range(m):
        temp = []
        for _ in range(n):
            temp.append(-1)
        result.append(temp)

    #Backtracking:
    if (not Assign_for_bruteforce(0, 0, m, n, result, mat)):
        for row in range(m):
            for col in range(n):
                result[row][col] = -1

    end = perf_counter()
    
    return result, end - start


def main():
    # read the input from the input file:
    m, n, mat = readfile("input.txt")

    # using pysat:
    result_pysat, runtime_pysat = Pysat_ver(m, n, mat)
    printMatrix(result_pysat)
    print("Execution time:", runtime_pysat, 's')

    print()

    # using backtrack:
    result_backtrack, runtime_backtrack = Backtracking_ver(m, n, mat)
    printMatrix(result_backtrack)
    print("Execution time:", runtime_backtrack, 's')

    print()

    result_bruteforce, runtime_bruteforce = Brute_Force_ver(m, n, mat)
    printMatrix(result_bruteforce)
    print("Execution time:", runtime_bruteforce, 's')

    print()


    # adj_cell = get_adjacent_cells(mat, 10, 10, 0, 5)
    # print(adj_cell)
    # print(uniquify_CNF_clauses(gen_clauses(mat[0][5], adj_cell)))
    # if ([-15] in clauses):
    #     print('yeys')
    # write_file("output.txt", solution)


if __name__ == "__main__":
    main()

from CNF import *


def main():
    # read the input from the input file:
    m, n, mat = readfile("input.txt")

    # pysat:
    result_pysat, runtime_pysat = pysatSolving(m, n, mat)
    print("PySAT matrix:")
    printMatrix(result_pysat)
    print("Amount of time the algorithm spent:", runtime_pysat, 'second(s).')
    print()

    # backtrack:
    result_backtrack, runtime_backtrack = Backtracking_ver(m, n, mat)
    print("Backtrack algorithm's matrix:")
    printMatrix(result_backtrack)
    print("Amount of time the algorithm spent:", runtime_backtrack, 'second(s).')
    print()

    # brute force
    result_bruteforce, runtime_bruteforce = Brute_Force_ver(m, n, mat)
    print("Brute-force algorithm's matrix:")
    printMatrix(result_bruteforce)
    print("Amount of time the algorithm spent:", runtime_bruteforce, 'second(s).')

    print()


    # adj_cell = get_adjacent_cells(mat, 10, 10, 0, 5)
    # print(adj_cell)
    # print(uniquify_CNF_clauses(gen_clauses(mat[0][5], adj_cell)))
    # if ([-15] in clauses):
    #     print('yeys')
    # write_file("output.txt", solution)


if __name__ == "__main__":
    main()

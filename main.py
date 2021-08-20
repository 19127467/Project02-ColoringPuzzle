from CNF import *


if __name__ == "__main__":
    m, n, mat = readfile("input.txt")
# PySAT
    result_pysat, runtime_pysat = use_pysat(mat,m, n)
    print("PySAT matrix:")
    printMatrix(result_pysat)
    print("Amount of time the algorithm spent:", runtime_pysat, 'second(s).')
    print()
# Backtrack:
    result_backtrack, runtime_backtrack = use_Backtracking(mat,m,n)
    print("Backtrack algorithm's matrix:")
    printMatrix(result_backtrack)
    print("Amount of time the algorithm spent:", runtime_backtrack, 'second(s).')
    print()
# Brute-force
    result_bruteforce, runtime_bruteforce = use_Brute_Force(mat,m,n)
    print("Brute-force algorithm's matrix:")
    printMatrix(result_bruteforce)
    print("Amount of time the algorithm spent:", runtime_bruteforce, 'second(s).')
    print()
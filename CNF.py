from time import perf_counter
from typing import List, Set, Dict, Tuple, Optional, Any
import os.path as path
from itertools import combinations
from time import perf_counter
from pysat.solvers import Glucose3


# Input
def readfile(file):
    if path.isfile(file)==False: return 'No file directory.'
    file=open(file)
    mat_size=file.readline().split(' ')
    s=file.readlines()
    s=[i.split(' ') for i in s]
    file.close()
    return int(mat_size[0]), int(mat_size[1]),[[int(num) for num in tmp]for tmp in s]


# Output
def printMatrix(mat):
    for row in mat:
        for i in row:
            print(i,end=' ')
        print()


# Find adjacent cells, then get the combination. After that, divide into True and False set.
# Parameter returns a list of CNF clause
def generateClauses(r, adjacentList):
    clauses = []
    for trueSet in combinations(adjacentList, r):
        falseSet = list(set(adjacentList) - set(trueSet))
        for item in trueSet: clauses.append([item] + falseSet)
        for item in falseSet: clauses.append([-item] + [-i for i in trueSet])
    return clauses


# Combine CNFs
def unifiedCNF_Clauses(mix_clauses):
    res = []
    for i in mix_clauses:
        if set(i) not in res: res.append(set(i))
    return res

# Find adjacent cells
def getAdjacent(m, n, row, col):
    adjacent_cell=[]
    for i in range(row-1, row+2):
        for j in range(col-1, col+2):
            if i >- 1 and i < m and j > -1 and j < n: adjacent_cell.append(i*n+j+1)
    return adjacent_cell

    # Backtrack algorithm (fixes and backups)
# Cell position
def getPosCells(mat, m, n):
    posCells=[]
    for row in range(m):
        for col in range(n):
            if mat[row][col] >= 0 and mat[row][col] <= 9: posCells.append((mat[row][col], row, col))
    return posCells


# CNF fetch
def getCNF_Clauses(input, m, n):
    clauses = []
    for i in range(0, m):
        for j in range(0, n):
            if input[i][j] > -1:
                adjacent_list=getAdjacent(m, n, i, j)
                clauses=clauses+generateClauses(input[i][j], adjacent_list)
    return clauses

def completeClauses(mat, m, n):
    return unifiedCNF_Clauses(getCNF_Clauses(mat, m, n))


    # Main brute-force algorithm
# Test whether solution is successful
def testResult(input,m, n, result):
    for row in range(m):
        for col in range(n):
            if (input[row][col] >= 0 and input[row][col] <= 9):
                count_green, right_green = 0, int(input[row][col])
                for i in range(row - 1, row + 2):
                    if (i >= 0 and i < m):
                        for j in range(col - 1, col + 2):
                            if (j >= 0 and j < n):
                                if(result[i][j] == 1):
                                    count_green += 1
                if (right_green != count_green):
                    return False
    return True


# Mark color of a cell using brute-force algorithm
def BFAssignment(row, col, input, m, n, result):
    if (row == m):
        return testResult(input, m, n, result)
    for color in range(2):
        result[row][col] = color
        next_row, next_col = row, col + 1
        if (next_col == n):
            next_row += 1
            next_col = 0
        if (BFAssignment(next_row, next_col, input, m, n, result)):
            return True
    return False



# Solve matrix input brute-force
def use_Brute_Force(mat, m, n):
    start = perf_counter()
    result = [[0 for i in range(n)]for j in range(m)]
    if (not BFAssignment (0, 0, mat, m, n, result)):
        for row in range(m):
            for col in range(n): result[row][col]=-1
    end = perf_counter()
    return result, end - start


    # Main backtrack algorithm
# Get red cells in checked areas
def checkRedAdjCell(checkCell, m, n, result):
    redAdjList = []
    countRedAdjCells, totalAdjCell = 0, 0
    for i in range(checkCell[1]-1, checkCell[1]+2):
        if (i >= 0 and i < m):
            for j in range(checkCell[2]-1, checkCell[2]+2):
                if (j >= 0 and j < n):
                    if (result[i][j] == 0):
                        countRedAdjCells += 1
                        redAdjList.append((i, j))
                    totalAdjCell += 1

    return (totalAdjCell, countRedAdjCells, redAdjList)


# Mark cell green using backtrack algorithm
def BTAssignment(indexCell, posCell, redAdjIndex, redAdj, green, input, m, n, result):
    for adj in range(redAdjIndex, redAdj[1]):
        result[redAdj[2][adj][0]][redAdj[2][adj][1]] = 1
        conflict = 0
        for i in range(0, indexCell):
            temp = checkRedAdjCell(posCell[i], m, n, result)
            temp2 = int(posCell[i][0]) - (temp[0] - temp[1])
            if (temp2 != 0):
                conflict = 1
                break
        if (conflict == 0):
            green -= 1
            if (green > 0):
                if(BTAssignment(indexCell, posCell, adj+1, redAdj, green, input, m, n, result)):
                    return True
            elif(green == 0):
                if (solveBTCells(indexCell+1, posCell, input, m, n, result)):
                    return True
            green += 1
        result[redAdj[2][adj][0]][redAdj[2][adj][1]] = 0
    return False


# Consider suitable color for the area of solved cell:
def solveBTCells(index, posCell, input, m, n, result):
    if (index < len(posCell)):
        redAdj = checkRedAdjCell(posCell[index], m, n, result)
        green = int(posCell[index][0]) - (redAdj[0] - redAdj[1])
        if (green > 0):
            return BTAssignment(index, posCell, 0, redAdj, green, input, m, n, result)
        elif (green == 0):
            return solveBTCells(index+1, posCell, input, m, n, result)
        else: return False
    return True


# Solve matrix input backtrack
def use_Backtracking(mat, m, n):
    start = perf_counter()
    result = [[0 for i in range(n)]for j in range(m)]
    cell_with_unnega_value = getPosCells(mat, m, n)
    if (not solveBTCells(0, cell_with_unnega_value, mat, m, n, result)):
        for row in range(m):
            for col in range(n): result[row][col]=-1
    end = perf_counter()
    return result, end - start


    # Main PySAT
# Solve matrix input pySAT
def use_pysat(mat, m, n):
    result = []
    start = perf_counter()
    clauses = completeClauses(mat, m, n)
    glucose = Glucose3()
    for i in clauses: glucose.add_clause([int(k) for k in i])
    glucose.solve()
    model = glucose.get_model()
    result = [[1 if (i*n + j + 1) in model else 0 for j in range(n)]for i in range(m)]
    stop = perf_counter()
    return result, stop - start


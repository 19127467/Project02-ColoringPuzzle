from time import perf_counter


#Function for reading the input file:
def Read_file(filename: str):
    matrix = []
    try: #Check wether we can open the file or not
        file = open(filename)

    except: #The file at the given url cannot openned:
        print("Error: Cannot open the file.\nPlease check if it was moved or deleted.\n")

    else: #Openned file succeed:
        content = file.read().rsplit('\n')
        file.close()

        #Convert the content into a string matrix:
        abs_index_matrix = []
        abs_index = 0
        for i in content:
            row, index_of_row, temp = [], [], i.rsplit(' ')
            for j in temp:
                row.append(j)
                index_of_row.append(abs_index)
                abs_index += 1
            matrix.append(row)
            abs_index_matrix.append(index_of_row)

    return matrix, abs_index_matrix


#Function for printing matrix:
def Print_matrix(matrix: list):
    for row in matrix:
        print(row)


#Function for checking if the result is a right soluion:
def Test_result(puzzle: list, result: list):
    nrow, ncol = len(puzzle), len(puzzle[0])
    for row in range(nrow):
        for col in range(ncol):
            if (puzzle[row][col] in "0123456789"):
                count_green, right_green = 0, int(puzzle[row][col])
                for i in range(row - 1, row + 2):
                    if (i >= 0 and i < nrow):
                        for j in range(col - 1, col + 2):
                            if (j >= 0 and j < ncol):
                                if(result[i][j] == 1):
                                    count_green += 1
                if (right_green != count_green):
                    return False
    return True


#Function for assignning color to each cell in Brute Force algorithm:
def Assign_for_bruteforce(row: int, col: int, nrow: int, ncol: int, result: list, puzzle: list):
    if (row == nrow):
        return Test_result(puzzle, result)
    for color in range(2):
        result[row][col] = color
        next_row, next_col = row, col + 1
        if (next_col == ncol):
            next_row += 1
            next_col = 0
        if (Assign_for_bruteforce(next_row, next_col, nrow, ncol, result, puzzle)):
            return True
    return False


#Function for solving puzzle by using Brute Force algorithm:
def Brute_Force_ver(puzzle: list):
    #prepare needed variables:
    start = perf_counter()
    nrow, ncol = len(puzzle), len(puzzle[0])
    result = []
    for _ in range(nrow):
        temp = []
        for _ in range(ncol):
            temp.append(-1)
        result.append(temp)

    #Backtracking:
    if (not Assign_for_bruteforce(0, 0, nrow, ncol, result, puzzle)):
        for row in range(nrow):
            for col in range(ncol):
                result[row][col] = -1
    
    end = perf_counter()

    return result, end - start


def clause_generate(row: int, col: int, nrow: int, ncol: int, puzzle: list):
    clauses = []
    nchoosed = int(puzzle[row][col])
    check_cell = [row, col]
    for i in range(row-1, row+2):
        if (i >=0 and i < nrow):
            for j in range(col-1, col+2):
                if (j >= 0 and j < ncol):
                    #Do sth here
                    a=5

    return clauses                    


def Get_CNF(puzzle: list):
    CNF_clause = []
    nrow, ncol = len(puzzle), len(puzzle[0])
    for row in range(nrow):
        for col in range(ncol):
            if (len(puzzle[row][col]) == 1 and puzzle[row][col] in "123456789"):
                CNF_clause.append(clause_generate(row, col, nrow, ncol, puzzle))

    return CNF_clause


if __name__ == "__main__":
    puzzle, abs_index_matrix = Read_file("input.txt")
    print("Puzzle:")
    Print_matrix(puzzle)
    print("Index of each cell:")
    Print_matrix(abs_index_matrix)
    print()
    
    BF_result, BF_runtime = Brute_Force_ver(puzzle)
    print("Result of Brute Force algorithm:")
    Print_matrix(BF_result)
    print("Run time of Brute Force:", BF_runtime)
    
import random 

def binary_matrix(size):
    matrix = [ [ 0 for y in range( size + 2 ) ]
             for x in range( size + 2 ) ]

    for i in range(0, size + 2): 
        for j in range(0, size + 2):
            if(i == 0 or j == 0 or i == size + 1 or j == size + 1):
                matrix[i][j] = 0
            else:
                matrix[i][j] = random.randrange(0,2)
    return matrix 
 
def count_true(matrix, size):
    result = [ [0 for y in range(size)]
                for x in range(size)]
    for i in range(1, len(matrix) - 1):
        for j in range(1, len(matrix) - 1):
            result[i - 1][j - 1] = matrix[i][j] + matrix[i-1][j] + matrix[i + 1][j] + matrix[i][j + 1] +matrix[i][j - 1] +matrix[i + 1][j + 1] +matrix[i - 1 ][j -1]+ matrix[i + 1][j - 1] + matrix[i - 1][j + 1]
    return result 

def write_file(result, no): 
    f = open(str(len(result)) + str(no) + ".txt", "w")
    f.write(str(len(result)) +"\n"+  str(len(result)) + "\n")
    for i in range(0, len(result)): 
        for j in range(0, len(result)):
            f.write(str(result[i][j]) + ' ')
        f.write("\n")
    f.close 

def main():
    size = 11
    no = 5 # stt test case 
    m = count_true(binary_matrix(size), size)
    write_file(m, no)
    for no in range(1, 6): 
        m = count_true(binary_matrix(size), size)
        write_file(m, no)
main()
from typing import List, Set, Dict, Tuple, Optional, Any
from time import perf_counter
from itertools import combinations
import tkinter as tkt
from tkinter import filedialog


# function to read the input file:
def read_file(file_name_in: str) -> Tuple[int, int, List[int]]:
    matrix = []
    try: #Check wether we can open the file or not
        file = open(file_name_in)

    except: #The file at the given url cannot openned:
        print("Error: Cannot open the file.\nPlease check if it was moved or deleted.\n")

    else: #Openned file succeed:
        content = file.read().rsplit('\n')
        file.close()

        #Convert the content into a string matrix:
        m, n = int(content[0]), int(content[1])
        for line in content:
            if(line != content[0] and line != content[1]):
                row, temp = [], line.rsplit(' ')
                for num in temp:
                    row.append(int(num))
                matrix.append(row)

    return m, n, matrix


def write_file(file_name_out: str, result: str) -> None:
    with open(file_name_out, 'w') as fout:
        fout.write(result)


def print_matrix(matrix: List[List[int]]) -> None:
    for row in matrix:
        [print(_, end=' ') if _ > -1 else print('.', end=' ') for _ in row]
        print('')


# get adjacent
# get combination
# split 2 group
def gen_clauses(r: int, list_adj_cells: List[int]) -> List[List[int]]:
    clauses = []
    for true_group in combinations(list_adj_cells, r):
        false_group = list(set(list_adj_cells) - set(true_group))
        for item in true_group:
            clauses.append([item] + false_group)

        for item in false_group:
            clauses.append([-item] + [-_ for _ in true_group])

    return clauses


def get_adjacent_cells(matrix: List[List[int]], m: int, n: int, i: int, j: int) -> List[int]:
    list_adj_cells = []
    for adj_i in range(i - 1, i + 2):
        for adj_j in range(j - 1, j + 2):
            if (adj_i > -1) and (adj_i < m) and (adj_j > -1) and (adj_j < n):
                list_adj_cells.append(adj_i * n + adj_j + 1)
    return list_adj_cells


def get_clauses(puzzle: List[List[int]], m: int, n: int) -> List[List[int]]:
    clauses = []
    for i in range(m):
        for j in range(n):
            if puzzle[i][j] > -1:
                list_adj_cells = get_adjacent_cells(puzzle, m, n, i, j)
                clauses += gen_clauses(puzzle[i][j], list_adj_cells)
    return clauses


def uniquify_CNF_clauses(clauses: List[List[int]]) -> List[Set[int]]:
    uniq = []
    for _ in clauses:
        if set(_) not in uniq:
            uniq.append(set(_))
    return uniq


def final_CNF_clauses(mat: List[int], m: int, n: int):
    clauses = get_clauses(mat, m, n)
    # print(clauses)
    print('#clauses:', len(list(clauses)))
    clauses = uniquify_CNF_clauses(clauses)
    print('#clauses:', len(list(clauses)))
    # print(clauses)
    return clauses


#For Backtracking only:
def get_cells_with_unnega_val(m: int, n: int, matrix: List[int]) -> List[Tuple[int, int, int]]:
    cell_with_unnega_value = []
    for row in range(m):
        for col in range(n):
            if (matrix[row][col] >= 0 and matrix[row][col] <= 9):
                cell_with_unnega_value.append((matrix[row][col], row, col))
    return cell_with_unnega_value


#Function for getting the information of all red cells in the area of the checked cell:
def Check_red_adjcell(check_cell: Tuple[int, int, int], m: int, n: int, result: list):
    red_Adjcell_list = []
    count_red_adjcell, total_adjcell = 0, 0
    for i in range(check_cell[1]-1, check_cell[1]+2):
        if (i >= 0 and i < m):
            for j in range(check_cell[2]-1, check_cell[2]+2):
                if (j >= 0 and j < n):
                    if (result[i][j] == 0):
                        count_red_adjcell += 1
                        red_Adjcell_list.append((i, j))
                    total_adjcell += 1
    
    return (total_adjcell, count_red_adjcell, red_Adjcell_list)


#Function for assignning green color to the 
def Assign_for_backtrack(cell_index: int, cell_with_unnega_value: List[Tuple[int, int, int]],
                         red_adj_index: int, red_Adj_info:tuple, need_green: int, m: int, n: int, result: list, puzzle: list):

    for adj in range(red_adj_index, red_Adj_info[1]):
        result[red_Adj_info[2][adj][0]][red_Adj_info[2][adj][1]] = 1
        conflict = 0
        for i in range(0, cell_index):
            temp = Check_red_adjcell(cell_with_unnega_value[i], m, n, result)
            temp2 = int(cell_with_unnega_value[i][0]) - (temp[0] - temp[1])
            if (temp2 != 0):
                conflict = 1
                break
        if (conflict == 0):
            need_green -= 1
            if (need_green > 0):
                if(Assign_for_backtrack(cell_index, cell_with_unnega_value, adj+1, red_Adj_info, need_green, m, n, result, puzzle)):
                    return True
            elif(need_green == 0):
                if (Solve_cell_backtrack(cell_index+1, cell_with_unnega_value, m, n, result, puzzle)):
                    return True
            need_green += 1
        result[red_Adj_info[2][adj][0]][red_Adj_info[2][adj][1]] = 0
    return False


#Function for finding the right color for the area of the checked cell:
def Solve_cell_backtrack(index: int, cell_with_unnega_value: List[Tuple[int, int, int]], m: int, n: int, result: list, puzzle: list):
    if (index < len(cell_with_unnega_value)):
        red_Adj_info = Check_red_adjcell(cell_with_unnega_value[index], m, n, result)
        need_green = int(cell_with_unnega_value[index][0]) - (red_Adj_info[0] - red_Adj_info[1])
        if (need_green > 0):
            return Assign_for_backtrack(index, cell_with_unnega_value, 0, red_Adj_info, need_green, m, n, result, puzzle)
        elif (need_green == 0):
            return Solve_cell_backtrack(index+1, cell_with_unnega_value, m, n, result, puzzle)
        else: return False
    return True


#For Brute Force only:
def Test_result(m: int, n: int, puzzle: List[int], result: List[int]):
    for row in range(m):
        for col in range(n):
            if (puzzle[row][col] >= 0 and puzzle[row][col] <= 9):
                count_green, right_green = 0, int(puzzle[row][col])
                for i in range(row - 1, row + 2):
                    if (i >= 0 and i < m):
                        for j in range(col - 1, col + 2):
                            if (j >= 0 and j < n):
                                if(result[i][j] == 1):
                                    count_green += 1
                if (right_green != count_green):
                    return False
    return True


#Function for assignning color to each cell in Brute Force algorithm:
def Assign_for_bruteforce(row: int, col: int, m: int, n: int, result: List[int], puzzle: List[int]):
    if (row == m):
        return Test_result(m, n, puzzle, result)
    for color in range(2):
        result[row][col] = color
        next_row, next_col = row, col + 1
        if (next_col == n):
            next_row += 1
            next_col = 0
        if (Assign_for_bruteforce(next_row, next_col, m, n, result, puzzle)):
            return True
    return False


#For GUI only:
#Function for notifying an occurred error:
def Error_notification(error_mess: str):
    error_window = tkt.Toplevel()
    noti = tkt.Label(error_window, height=7, text=error_mess)
    noti.pack(padx=5)
    exit_but = tkt.Button(error_window, width=10, text="OK", command=error_window.destroy)
    exit_but.pack()


#Function for browsing the input file:
def Browse_file():
    #Prepare needed variables:
    global filename, puzzle, nrow, ncol
    puzzle = []

    #Get the url of the file:
    filename = filedialog.askopenfilename()

    if (len(filename) > 0): #If user choose a file.
    #Check if input is ok or not:
        puzzle, _ = read_file(filename)
        if(len(puzzle) == 0):
            filename = ""
            Error_notification("Error: Cannot open the file. Please check if it was moved or deleted.")
        else:
            nrow, ncol = len(puzzle), len(puzzle[0])
            #Check if the input is a right puzzle:
            for i in puzzle:
                if(len(i) != ncol):
                    puzzle.clear()
                    print("Error: The column of each row of the matrix must equal to each others.\n")
                    Error_notification("Error: The column of each row of the matrix must equal to each others.")
                    return

            #Display the url of the file on the screen
            file_entry.configure(state="normal")
            file_entry.delete(0,"end")
            file_entry.insert(0,filename)
            file_entry.configure(state="disable")

            #Enable the start button:
            start_but.configure(state="normal")


#Function for generating items of frame1:
def Frame1_content():
    global frame1, file_entry, start_but

    #For browsing file:
    #Label:
    label_browse = tkt.Label(frame1, text="Open file:                ")
    label_browse.grid(row=0, column=0, padx=2, pady=5,)
    #Entry:
    file_entry = tkt.Entry(frame1, width=100, state="disable")
    file_entry.grid(row=0, column=1, padx=10, pady=5)
    #Button:
    browse_but = tkt.Button(frame1, width=10, text="Browse", command=Browse_file)
    browse_but.grid(row=0, column=2, padx=2, pady=5)

    #For choosing algorithm:
    #Drop box menu:
    options = [" CNF with pysat ", "    CNF with A*   ", "     Brute-Force   ", "   Backtracking   "]
    choice = tkt.StringVar()
    choice.set(options[0])
    drop_menu = tkt.OptionMenu(frame1, choice, *options)
    drop_menu.grid(row=0, column=3, padx=2, pady=5)
    #Start button:
    start_but = tkt.Button(frame1, width=10, text="Start", state="disable")
    start_but.grid(row=1, column=3, padx=2, pady=5)

    #For updating state:
    #Label for updating:
    label_update = tkt.Label(frame1, text="Delay time:             ")
    label_update.grid(row=1, column=0, padx=2, pady=5,)
    #Entry:
    delay_time_entry = tkt.Entry(frame1, width=100)
    delay_time_entry.grid(row=1, column=1, padx=10., pady=5.)
    #Button:
    update_but = tkt.Button(frame1, width=10, text="Update")
    update_but.grid(row=1, column=2, padx=2, pady=7)

    #For showing step and heurstic:
    #Label:
    label_sh = tkt.Label(frame1, text="Step and heuristic:")
    label_sh.grid(row=2, column=0, padx=2, pady=5,)
    #Entry:
    sh_entry = tkt.Entry(frame1, width=100, state="disable")
    sh_entry.grid(row=2, column=1, padx=10, pady=5)


#Function for generating items of frame1:
def Frame2_content():
    global frame2, board_frame
    board_frame = tkt.Frame(frame2, bg="lightgrey")
    """ for i in range(30):
        label = tkt.Label(board_frame, text="0", bg="red", fg="white", width=4, height=1)
        label.grid(row=0, column=i, padx=1, pady=1) """
    #empty_board = tkt.Label
    for i in range(7):
        for j in range(7):
            color = "red" if j%2==0 else "blue"
            label = tkt.Label(board_frame, text=j, bg=color, fg="white", width=10, height=4)
            label.grid(row=i, column=j, padx=1, pady=0.5)
    
    board_frame.pack(padx=2)


#Main function for GUI:
def GUI():
    #Prepare needed variables:
    global myUI, frame1, frame2, file_entry, puzzle, filename

    #Create tkinter windows:
    myUI = tkt.Tk()
    myUI.title("Coloring Puzzle")
    myUI.geometry("980x690")

    #Command and input frame:
    frame1 = tkt.LabelFrame(myUI, bd=0)
    Frame1_content() #All text fields and buttons.
    frame1.pack()

    #Board frame:
    frame2 = tkt.LabelFrame(myUI, background="lightgrey", pady=5, bd=3)
    Frame2_content() #Board of the puzzle.
    frame2.pack(fill="x", pady=(10,0))

    myUI.mainloop()

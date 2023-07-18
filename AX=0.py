# Write a program in Python to solve the homogenous system Ax=0 and write the general solution in parametric vector form.
# Your program should accept as input the size of the matrix, i.e. the number of rows and the number of columns of A, and also the entries of A.
# The input should ideally be read from a text file, but if you haven't learnt how to do this, you may hard-code your input, as long as you are able to explain to your TA how to change the input to your program.
# Your code should be based on algorithms learned in the course. No pre-existing routines from Python libraries should be used.


def return_matrix(f_name):
    # in my text file, the first line contains no. of rows and no. of columns of the matrix respectively separated by a comma
    # next lines contain each row of the matrix with space separated values

    lst = []
    with open(f_name) as f:
        for c in f:
            lst.append([float(ele) for ele in (c.strip()).split()])
        # m -> no. of rows and n-> no. f columns
        m, n = len(lst), len(lst[0])  # dimensions of our matrix
    return lst, m, n


# Function to find REF of a matrix with total rows & columns as row,col and starting row, column as st_row,st_col
def REF(matrix, row, col, st_row, st_col):
    global pivot_lst
    rem_row = row-st_row
    rem_col = col-st_col
    # If no rows or columns are left to be reduced
    if rem_row == 0 or rem_col == 0:
        return
    # If only one row is left to be reduced
    if rem_row == 1:
        for i in range(st_col, col):
            if matrix[st_row][i] != 0:
                pivot_lst.append((st_row, i))
                break
        return
    else:
        pivot = 0
        # Interchange rows to make 1st row as pivot row & find pivot value
        for j in range(st_col, col):
            for i in range(st_row, row):
                if matrix[i][j] != 0:
                    matrix[st_row], matrix[i] = matrix[i], matrix[st_row]
                    pivot_row = st_row
                    pivot_col = j
                    pivot_lst.append((pivot_row, pivot_col))
                    pivot = matrix[pivot_row][pivot_col]
                    break
            if pivot != 0:
                break

        # Create zeros in all positions below the pivot position
        for i in range(pivot_row + 1, row):
            num = matrix[i][pivot_col] / pivot
            for j in range(pivot_col, col):
                matrix[i][j] -= num * matrix[pivot_row][j]

        # Recursively find REF of the remaining sub-matrix
        REF(matrix, row, col, pivot_row+1, pivot_col+1)


# Function to find RREF of an REF matrix with rows & columns as row, col and with pivt positions as in pivot_lst
def RREF(matrix, row, col, pivot_lst):
    for i in range(len(pivot_lst)-1, -1, -1):
        pivot_row, pivot_col = pivot_lst[i][0], pivot_lst[i][1]
        num = matrix[pivot_row][pivot_col]
        # Scaling operation to make a pivot as 1
        for j in range(pivot_col, col):
            matrix[pivot_row][j] = matrix[pivot_row][j]/num
        # Create zeroes above each pivot
        for k in range(pivot_row-1, -1, -1):
            num = matrix[k][pivot_col]
            for j in range(pivot_col, col):
                matrix[k][j] -= num*matrix[pivot_row][j]
    return


# Function to print the general solution in parametric vector form
def sol_par_vector(matrix, row, col, pivot_lst):
    # If every column is a pivot column, only trivial solution exists
    if len(pivot_lst) == col:
        print("SOLUTION: Only trivial solution: [0", end='')
        for i in range(n-1):
            print(",0", end='')
        print("]")
        return
    else:
        pivot_row = []
        pivot_col = []
        non_pivot_col = []
        free_var = []
        no_pivot = len(pivot_lst)
        sol = [[0 for _ in range(col)] for _ in range(col-no_pivot)]

        for i in range(no_pivot):
            pivot_row.append(pivot_lst[i][0])
            pivot_col.append(pivot_lst[i][1])

        for i in range(col):
            if i not in pivot_col:
                non_pivot_col.append(i)
                free_var.append('X_'+str(i))

        for i in range(len(non_pivot_col)):
            for j in range(col):
                if non_pivot_col[i] == j:
                    sol[i][j] = 1

        for i in range(len(non_pivot_col)):
            k = 0
            for j in pivot_col:
                sol[i][j] = (-1)*matrix[pivot_row[k]][non_pivot_col[i]]
                k += 1

        # Print the solution
        print("SOLUTION:")
        print("[0", end='')
        for i in range(n-1):
            print(",0", end='')
        print("]", end='')
        for i in range(len(non_pivot_col)):
            print(" +", free_var[i], "*", sol[i], end='')
        print('\n')


# Main Program
matrix, m, n = return_matrix("2022073_Aniket/matrix.txt")
pivot_lst = []
zero_matrix = True
for i in range(m):
    for j in range(n):
        if matrix[i][j] != 0:
            zero_matrix = False
            break
    if not zero_matrix:
        break
if zero_matrix:
    print("Any Vector in R(", n, ") is a solution.")
else:
    REF(matrix, m, n, 0, 0)
    print()
    print("PIVOT POSITION:", pivot_lst)
    print()
    RREF(matrix, m, n, pivot_lst)
    print("RREF:")
    for c in matrix:
        print(*c)
    print()
    sol_par_vector(matrix, m, n, pivot_lst)

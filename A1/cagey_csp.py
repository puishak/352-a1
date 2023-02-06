# =============================
# Student Names:
# Group ID:
# Date:
# =============================
# CISC 352 - W23
# cagey_csp.py
# desc:
#

#Look for #IMPLEMENT tags in this file.
'''
All models need to return a CSP object, and a list of lists of Variable objects
representing the board. The returned list of lists is used to access the
solution.

For example, after these three lines of code

    csp, var_array = binary_ne_grid(board)
    solver = BT(csp)
    solver.bt_search(prop_FC, var_ord)

var_array is a list of all variables in the given csp. If you are returning an entire grid's worth of variables
they should be arranged in a linearly, where index 0 represents the top left grid cell, index n-1 represents
the top right grid cell, and index (n^2)-1 represents the bottom right grid cell. Any additional variables you use
should fall after that (i.e., the cage operand variables, if required).

1. binary_ne_grid (worth 10/100 marks)
    - A model of a Cagey grid (without cage constraints) built using only
      binary not-equal constraints for both the row and column constraints.

2. nary_ad_grid (worth 10/100 marks)
    - A model of a Cagey grid (without cage constraints) built using only n-ary
      all-different constraints for both the row and column constraints.

3. cagey_csp_model (worth 20/100 marks)
    - a model of a Cagey grid built using your choice of (1) binary not-equal, or
      (2) n-ary all-different constraints for the grid, together with Cagey cage
      constraints.


Cagey Grids are addressed as follows (top number represents how the grid cells are adressed in grid definition tuple);
(bottom number represents where the cell would fall in the var_array):
+-------+-------+-------+-------+
|  1,1  |  1,2  |  ...  |  1,n  |
|       |       |       |       |
|   0   |   1   |       |  n-1  |
+-------+-------+-------+-------+
|  2,1  |  2,2  |  ...  |  2,n  |
|       |       |       |       |
|   n   |  n+1  |       | 2n-1  |
+-------+-------+-------+-------+
|  ...  |  ...  |  ...  |  ...  |
|       |       |       |       |
|       |       |       |       |
+-------+-------+-------+-------+
|  n,1  |  n,2  |  ...  |  n,n  |
|       |       |       |       |
|n^2-n-1| n^2-n |       | n^2-1 |
+-------+-------+-------+-------+

Boards are given in the following format:
(n, [cages])

n - is the size of the grid,
cages - is a list of tuples defining all cage constraints on a given grid.


each cage has the following structure
(v, [c1, c2, ..., cm], op)

v - the value of the cage.
[c1, c2, ..., cm] - is a list containing the address of each grid-cell which goes into the cage (e.g [(1,2), (1,1)])
op - a flag containing the operation used in the cage (None if unknown)
      - '+' for addition
      - '-' for subtraction
      - '*' for multiplication
      - '/' for division
      - '?' for unknown/no operation given

An example of a 3x3 puzzle would be defined as:
(3, [(3,[(1,1), (2,1)],"+"),(1, [(1,2)], '?'), (8, [(1,3), (2,3), (2,2)], "+"), (3, [(3,1)], '?'), (3, [(3,2), (3,3)], "+")])

'''

from cspbase import *

def binary_ne_grid(cagey_grid):
    """Return A csp model of a Cagey grid (without cage constraints) built using only binary not-equal constraints for
    both the row and column constraints.
    """
    n, _ = cagey_grid
    # Name for the csp model
    name = "binary_ne_{}".format(n)
    # Get all the cell variables in an nxn matrix
    cells = create_cell_variables(n)
    # Unflatten the matrix of cells to get an array of variables
    vars = []
    for row in cells:
        vars += row
    
    # Create the csp model object
    csp_model = CSP(name, vars)
    
    
    # Get all the binary satisfying tuples 
    binary_satisfying_tuples = []
    for i in range(1, n+1):
        for j in range(1, n+1):
            if i != j:
                binary_satisfying_tuples.append((i, j))

    # Constraints
    # Loop through all the cells in the grid and only create the necessary constraint for 
    # the upcoming rows and collumns, this will ensure that we don't create duplicate constraints
    # for each pair of cells
    for i in range(n):
        for j in range(n):
            # This portion is run on every cell on the grid
            # Set constraint for each element on the same col
            for ii in range(i+1, n):
                name = "bne[cell[{},{}], cell[{},{}]]".format(i+1, j+1, ii+1, j+1)
                con = Constraint(name, [cells[i][j], cells[ii][j]])
                con.add_satisfying_tuples(binary_satisfying_tuples)
                csp_model.add_constraint(con)
            # Set constraint for each element on the same row
            for jj in range(j+1, n):
                name = "bne[cell[{},{}], cell[{},{}]]".format(i+1, j+1, i+1, jj+1)
                con = Constraint(name, [cells[i][j], cells[i][jj]])
                con.add_satisfying_tuples(binary_satisfying_tuples)
                csp_model.add_constraint(con)
            
    return (csp_model, vars)

def nary_ad_grid(cagey_grid):
    """Return a csp model of a Cagey grid (without cage constraints) built using only n-ary all-different constraints
    for both the row and column constraints.
    """
    n, _ = cagey_grid
    # Name for the csp model
    name = "nary_ad_{}".format(n)
    # Get all the cell variables in an nxn matrix
    cells = create_cell_variables(n)
    
    # Unflatten the matrix of cells to get an array of variables
    vars = []
    for row in cells:
        vars += row
    
    # Create the csp model object
    csp_model = CSP(name, vars)
    
    # Get alll the satisfying tuples for an nary all diff constraint 
    nary_satisfying_tuples = get_nary_satisfying_tuples(n)
    
    # Constraints
    
    # Loop through 0 to n and create a constraint for each row and collumn
    for i in range(n):
        # The ith column
        col = []
        # The ith row
        row = []
        for j in range(n):
            col.append(cells[i][j])
            row.append(cells[j][i])
            
        # Create the column constraint 
        col_name = "all-dif-col({})".format(i)
        col_const = Constraint(col_name, col)
        col_const.add_satisfying_tuples(nary_satisfying_tuples)
        csp_model.add_constraint(col_const)
        # Create the row constraint
        row_name = "all-dif-row({})".format(i)
        row_const = Constraint(row_name, row)
        row_const.add_satisfying_tuples(nary_satisfying_tuples)
        csp_model.add_constraint(row_const)
    
    
    return (csp_model, vars)

def cagey_csp_model(cagey_grid):
    """Return A csp model built using n-ary all-different constraints for the grid, 
    together with cage constraints.
    """
    # Define the domain for the cage variables
    cage_domain = ["+", "-", "*", "/"]
    
    n, cages = cagey_grid
    # Get the csp_model from the nary_ad_grid function with all the cell variables and row and collumn 
    # constraints added to it
    csp_model, cell_flattened = nary_ad_grid(cagey_grid)
    
    # convert the flattened array of cells into a matrix of cell variables
    cell_variables = []
    for i in range(n):
        cell_variables.append(cell_flattened[i*n:(i+1)*n])
    
    # Create the a variable and constraint for each cage on the board
    for cage in cages:
        # Disect the cage into it's value, operations, and a list of all the cell positions
        value, cells, operation = cage
        
        # Create the text for the cells portion of the variable/constraint name
        cell_text = ""
        for cell in cells:
            cell_text += "Var-Cell({},{}), ".format(cell[0], cell[1])
        cell_text = "[{}]".format(cell_text.rstrip(", "))
        
        # Create the variable name
        var_name = "Cage_op({}:{}:{})".format(value, operation, cell_text)
        # create the constraints name
        con_name = "Cage_constraint({}:{}:{})".format(value, operation, cell_text)
        
        # Create the cage variable using the name we just created and the set the domain to 
        # all the operation that are allowed
        var = Variable(var_name, cage_domain)
        # This is the array of Variable object in the scope of the constraint
        scope = [var]
        # For each cell in cells get the corresponding cell variable from the cell_variables matrix 
        # and add it to the scope list
        for cell in cells:
            i = cell[0] - 1
            j = cell[1] - 1
            scope.append(cell_variables[i][j])
        
        # Create the constraint
        con = Constraint(con_name, scope)
        
        # get all the satisfying tupples for this constraint
        cage_satisfying_tuples = get_cage_satisfying_tuples(n, value, len(cells), operation)
        # Add the satisfying tuples to the Constraint
        con.add_satisfying_tuples(cage_satisfying_tuples)
        # Add the variable and the constraint to the csp model
        csp_model.add_var(var)
        csp_model.add_constraint(con)
    
    return csp_model, csp_model.get_all_vars()

###
### Helper Functions
###

def get_cage_satisfying_tuples(n, total, num_cells, operation):
    """Return a complete list of all satisfying tuples for a cage constraint

    Args:
        n (int): the dimension of the board or the maximum int value for the cells
        total (int): The total value for the cage
        num_cells (int): Number of cells in this cage
        operation (str): The specified operation for the cage,

    Returns:
        list: List of all the satisfying tuples
    """
    # If the operation is not specified("?") than return all the satisfying for all the operations
    if operation == "?":
        add_tuples = get_cage_satisfying_tuples(n, total, num_cells, "+")
        sub_tuples = get_cage_satisfying_tuples(n, total, num_cells, "-")
        mul_tuples = get_cage_satisfying_tuples(n, total, num_cells, "*")
        div_tuples = get_cage_satisfying_tuples(n, total, num_cells, "/")
        
        return add_tuples + sub_tuples + mul_tuples + div_tuples
    else:
        output = []
        tuples = []
        # Call the respective function according to the operation to get all the combination 
        # of values that satisfies this cage adn store it in the tuples
        if operation == "+":
            tuples = get_add_satisfying_tuples(n, total, num_cells)
        elif operation == "-":
            tuples = get_subtract_satisfying_tuples(n, total, num_cells)
        elif operation == "*":
            tuples = get_multiplication_satisfying_tuples(n, total, num_cells)
        elif operation == "/":
            tuples = get_division_satisfying_tuples(n, total, num_cells)
        else: 
            return []
        
        for tup in tuples:
            # For each tuple get a all permutations of it
            tup_permuted = get_all_permutations(tup)
            for tp in tup_permuted:
                # For each permutation of tuple that satisfies the cage, 
                # add the operation to the beginning of the list, and add it to the output list
                final_tp = [operation] + tp
                if final_tp not in output:
                    output.append(final_tp)
        
        return output


def get_add_satisfying_tuples(n, total, num_cells, min_val = 1):
    """Return all combinations of tuples with length num_cells that contains int from min_val to n inclusive 
    that adds up to the total
    """
    # base case, if there is only 1 cell and the total is within the allowed range of integer, return the total
    if num_cells == 1:
        if total >= min_val and total <= n:
           return [[total]] 
    # If there are more than 1 cell, than take all the possible values for the first cell(this cell) and call 
    # the function recursively to get the values for all the rest of the cells. The min_val variable is used to 
    # make sure we don't waste time checking the same combination twice
    elif num_cells >= 2:
        num_remaining_cells = num_cells - 1
        # Since each cell must contain atleast 1, 
        # the value of the first cell cannot be higher than value - number of remaining cells
        max_val = min(n, total - num_remaining_cells)
        output = []
        # Go through each possible value for the first cell
        for value in range(min_val, max_val + 1):
            # Recursively check if a solution is possible with this value for the first cell 
            rec = get_add_satisfying_tuples(n, total - value, num_remaining_cells, value)
            # Add the value for the current cell at the beginning of each solution and append it to the output list
            for sol in rec:
                output.append([value] + sol)
                    
        return output
    
    return []

def get_subtract_satisfying_tuples(n, total, num_cells, min_val = 1):
    """Return all combinations of tuples with length num_cells that contains int from min_val to n inclusive 
    that satisfies the cage using subtraction
    """
    # base case, if there is only 1 cell and the total is within the allowed range of integer, return the total
    if num_cells == 1:
        if total >= 1 and total <= n:
           return [[total]] 
    # If there are more than 1 cell, than take all the possible values for the first cell(this cell) and call 
    # the function recursively to get the values for all the rest of the cells. The min_val variable is used to 
    # make sure we don't waste time checking the same combination twice
    elif num_cells >= 2:
        num_remaining_cells = num_cells - 1
        # Since each cell has to have a value of 1, this cell must have 
        # a value greater than or equal to total + num_remaining_cells
        # There are no solutions if min_val is greater than n
        output = []
        for value in range(min_val, n + 1):
            # value - (new val) = total => (new val) = value - total
            rec = get_subtract_satisfying_tuples(n, value - total, num_remaining_cells, value)
            
            # Add the value for the current cell at the beginning of each solution and append it to the output list
            for sol in rec:
                output.append([value] + sol)
        return output
    return []

def get_multiplication_satisfying_tuples(n, total, num_cells, min_val = 1):
    """Return all combinations of tuples with length num_cells that contains int from min_val to n inclusive 
    that satisfies the cage using multiplication
    """
    # base case, if there is only 1 cell and the total is within the allowed range of integer, return the total
    if num_cells == 1:
        if total >= min_val and total <= n:
           return [[total]] 
    # Implemented similarly to the add function
    elif num_cells >= 2:
        num_remaining_cells = num_cells - 1
        # Since we are only multiplying positive integers value cannot be greater than total
        max_val = min(n, total)
        output = []
        for value in range(min_val, max_val + 1):
            # We will only consider value if total is divisible by it
            if total % value == 0:
                rec = get_multiplication_satisfying_tuples(n, total // value, num_remaining_cells, value)
                # Add the value for the current cell at the beginning of each solution and append it to the output list
                for sol in rec:
                    output.append([value] + sol)
        
        return output
    return []

def get_division_satisfying_tuples(n, total, num_cells, min_val = 1):
    """Return all combinations of tuples with length num_cells that contains int from min_val to n inclusive 
    that satisfies the cage using division
    """
    # base case, if there is only 1 cell and the total is within the allowed range of integer, return the total
    if num_cells == 1:
        if total >= min_val and total <= n:
           return [[total]] 
    # Implemented similarly to the subtract function
    elif num_cells >= 2:
        num_remaining_cells = num_cells - 1
        output = []
        for value in range(min_val, n + 1):
            # new / val = total => new = total * val
            rec = get_division_satisfying_tuples(n, value * total, num_remaining_cells, value)
            
            # Add the value for the current cell at the beginning of each solution and append it to the output list
            for sol in rec:
                output.append(sol + [value])
            
        return output
    
    return []
    
def get_all_permutations(lst):
    """Return all permutations of the list lst
    """
    l = len(lst)
    # Base case: If lst only contains 2 items
    if l == 2:
        return [lst, [lst[1], lst[0]]]
    # Recursive case: If lst has more than 2 items,
    elif l > 2:
        # The last item of the list is the current item
        curr = lst[-1]
        # Get all the permutations of the sublist without the current item
        permutations = get_all_permutations(lst[:-1])
        output = []
        for perm in permutations:
            # For each permutation of the sublist, insert the curr in every possible position
            # Done backward, so the output looks neat
            for i in range(l-1, -1, -1):
                new_perm = list(perm)
                new_perm.insert(i, curr)
                output.append(new_perm)
        return output
    else:
        return lst
        

def get_nary_satisfying_tuples(n):
    """Return a list of nary alldiff touples that satisfies our constraints for the board
    """
    lst = []
    # Create a list with all number from 1 to n inclusive
    for i in range(1, n+1):
        lst.append(i)
    # Get all the permutations of the list
    return get_all_permutations(lst)


def create_cell_variables(n):
    """Return nXn matrix of cell Variables with the proper domain and name
    """
    cells = []
    # Define the domain of each cell as all the numbers from 1 to n inclusive
    cell_domain = list(range(1, n+1))
    # Loop over the rows and columns and create a Variable object with the appropriate name 
    # and append it to the output list
    for i in range(n):
        row = []
        for j in range(n):
            cell = Variable("Cell({},{})".format(i+1,j+1), cell_domain)
            row.append(cell)
        cells.append(row)
        
    return cells

    
    

if __name__ == "__main__":
    # Sample grid to test our code
    sample_grid = (3, [(3,[(1,1), (2,1)],"+"),(1, [(1,2)], '?'), (8, [(1,3), (2,3), (2,2)], "+"), (3, [(3,1)], '?'), (3, [(3,2), (3,3)], "+")])
    # print(sample_grid)

    # model = binary_ne_grid(sample_grid)
    # model = nary_ad_grid(sample_grid)
    # model = cagey_csp_model(sample_grid)
    
    # Test get_add_satisfying_tuples
    # result = get_add_satisfying_tuples(6, 8, 3)
    # for r in result:
    #     print(r)
    
    # Test get_subtract_satisfying_tuples
    # result = get_subtract_satisfying_tuples(6, 6, 3)
    # for r in result:
    #     print(r)
    
    # Test get_multiplication_satisfying_tuples
    # result = get_multiplication_satisfying_tuples(6, 12, 3)
    # for r in result:
    #     k = get_all_permutations(r)
    #     for i in k:            
    #         print(i)    
    
    # Test get_division_satisfying_tuples
    # result = get_division_satisfying_tuples(6, 12, 3)
    # for r in result:
    #     print(r)

    # Test get_all_combinations
    # result = get_all_combinations([1, 2, 3, 4])
    # for r in result:
    #     print(r)
    
    # Test get_cage_satisfying_tuples
    # result = get_cage_satisfying_tuples(6, 4, 2, "?")
    # for r in result:
    #     print(r)
    
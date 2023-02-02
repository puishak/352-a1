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
import os

def binary_ne_grid(cagey_grid):
    ##IMPLEMENT
    return 0

def nary_ad_grid(cagey_grid):
    
    n, cages = cagey_grid
    
    name = "nary_ad_{}".format(n)
    cells = create_cell_variables(n)
    cage_vars = create_cage_variables(cages)
    
    vars = []
    for row in cells:
        vars += row
        
    vars += cage_vars
    
    # for v in vars:
    #     print(type(v))
    
    csp_model = CSP(name, vars)
    return csp_model

def cagey_csp_model(cagey_grid):
    ##IMPLEMENT
    pass
    

# Return nXn matrix of cell Variables with the proper domain and name
def create_cell_variables(n):
    cells = []
    cell_domain = list(range(1, n+1))
    for i in range(n):
        row = []
        for j in range(n):
            cell = Variable("Cell({},{})".format(i+1,j+1), cell_domain)
            row.append(cell)
        cells.append(row)
        
    return cells

# Return all the cage varibles for the cages
def create_cage_variables(cages):
    cage_domain = ["+", "-", "*", "/"]
    cage_vars = []
    
    for cage in cages:
        v, cells, op = cage
        cell_text = ""
        
        for cell in cells:
            cell_text += "Var-Cell({},{}), ".format(cell[0], cell[1])
        cell_text = "[{}]".format(cell_text.rstrip(", "))
        
        
        var_name = "Cage_op({}:{}:{})".format(v, op, cell_text)
        
        cage_vars.append(Variable(var_name, cage_domain))
        
    return cage_vars
    
    

if __name__ == "__main__":
    # Sample grid to test our code
    sample_grid = (3, [(3,[(1,1), (2,1)],"+"),(1, [(1,2)], '?'), (8, [(1,3), (2,3), (2,2)], "+"), (3, [(3,1)], '?'), (3, [(3,2), (3,3)], "+")])
    # print(sample_grid)
    

    # model = binary_ne_grid(sample_grid)
    model = nary_ad_grid(sample_grid)
    # model = cagey_csp_model(sample_grid)
    
    
    for var in model.get_all_vars():
        print(var)
        
    # for con in model.get_all_cons():
    #     print(con)

    # temp = create_cell_variables(3)

    # for i in temp:
    #     for j in i:
    #         print(j.domain())
    
    # b = create_cage_variables(sample_grid[1])
    # for t in b:
    #     print(t.domain())
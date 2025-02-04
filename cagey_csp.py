# =============================
# Student Names: Corey McCann
# Group ID: 43
# Date: 01/28/2025
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

var_array is a list of all Variables in the given csp. If you are returning an entire grid's worth of Variables
they should be arranged linearly, where index 0 represents the top left grid cell, index n-1 represents
the top right grid cell, and index (n^2)-1 represents the bottom right grid cell. Any additional Variables you use
should fall after that (i.e., the cage operand variables, if required).

1. binary_ne_grid (worth 0.25/3 marks)
    - A model of a Cagey grid (without cage constraints) built using only
      binary not-equal constraints for both the row and column constraints.

2. nary_ad_grid (worth 0.25/3 marks)
    - A model of a Cagey grid (without cage constraints) built using only n-ary
      all-different constraints for both the row and column constraints.

3. cagey_csp_model (worth 0.5/3 marks)
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
from itertools import combinations, permutations, product
from math import prod

def binary_ne_grid(cagey_grid):
    # create variable objects for each cell in the grid with a domain of 1-n and add
    # these variables to a csp object
    n = cagey_grid[0]
    domain = [i for i in range(1, n + 1)]
    variables = []
    csp = CSP("Cagey Grid")
    
    # if we keep the variables structured much like a grid it will make accessing and returning them easier later
    for i in range(n):
        row = []
        for j in range(n):
            new_variable = Variable(f"Cell({i + 1},{j + 1})", domain)
            row.append(new_variable)
        variables.append(row)

    # add each variable to the csp object
    for row in variables:
        for var in row:
            csp.add_var(var)
            
    # for every pair of variables in the same row, add a binary not-equal constraint
    for i in range(n):
        row_vars = variables[i]
        
        for var1, var2 in combinations(row_vars, 2):
            constraint = Constraint(f"C_{var1.name}_{var2.name}", [var1, var2])
            
            satisfying_tuples = [(a, b) for a in var1.domain() for b in var2.domain() if a != b]
                        
            constraint.add_satisfying_tuples(satisfying_tuples)
            csp.add_constraint(constraint)       
    
    # for every pair of variables in the same coloumn, add a binary not-equal constraint
    for j in range(n):
        col_vars = [variables[row][j] for row in range(n)]
        
        for var1, var2 in combinations(col_vars, 2):
            constraint = Constraint(f"C_{var1.name}_{var2.name}", [var1, var2])
            
            satisfying_tuples = [(a, b) for a in var1.domain() for b in var2.domain() if a != b]
            
            constraint.add_satisfying_tuples(satisfying_tuples)
            csp.add_constraint(constraint)
    
    return csp, variables   

def nary_ad_grid(cagey_grid):
    # create variable objects for each cell in the grid with a domain of 1-n and add
    # these variables to a csp object
    n = cagey_grid[0]
    domain = [i for i in range(1, n + 1)]
    variables = []
    csp = CSP("Cagey Grid")
    
    # if we keep the variables structured much like a grid it will make accessing and returning them easier later
    for i in range(n):
        row = []
        for j in range(n):
            new_variable = Variable(f"Cell({i + 1},{j + 1})", domain)
            row.append(new_variable)
        variables.append(row)

    # add each variable to the csp object
    for row in variables:
        for var in row:
            csp.add_var(var)
            
    # for each row we create an all-diff constraint involving all variables in that row
    for i in range(n):
        row_vars = variables[i]
        
        constraint = Constraint(f"C_row{i}", row_vars)
        
        satisfying_tuples = list(permutations([i for i in range(1, n + 1)], len(row_vars)))
        
        constraint.add_satisfying_tuples(satisfying_tuples)
        csp.add_constraint(constraint)
        
    # for each column we create an all-diff constraint involving all variables in that column
    for i in range(n):
        col_vars = [variables[j][i] for j in range(n)]
        
        constraint = Constraint(f"C_column{i}", col_vars)
        
        satisfying_tuples = list(permutations([i for i in range(1, n + 1)], len(col_vars)))
        
        constraint.add_satisfying_tuples(satisfying_tuples)
        csp.add_constraint(constraint)
    
    return csp, variables


def cagey_csp_model(cagey_grid):
    # Build the base CSP using binary_ne_grid
    n = cagey_grid[0]
    csp, var_matrix = binary_ne_grid(cagey_grid)

    # For each cage, create an operator variable and a constraint linking it to its cells
    board = cagey_grid[1]
    for cage in board:
        target   = cage[0]
        cell_pos = cage[1]
        operator = cage[2]

        # Determine operator domain (either a single known operator or all four if '?')
        op_domain = ['+', '-', '*', '/'] if operator == '?' else [operator]

        # Name the cage variable according to the puzzle's format
        cage_name = f"Cage_op({target}:{operator}:["
        cage_name += ", ".join(f"Var-{var_matrix[r-1][c-1].name}" for (r,c) in cell_pos)
        cage_name += "])"

        cage_var = Variable(cage_name, op_domain)
        csp.add_var(cage_var)

        # Create a constraint whose scope includes the cage_var and all cell variables in this cage
        cage_cells = [var_matrix[r-1][c-1] for (r,c) in cell_pos]
        scope_vars = [cage_var] + cage_cells
        constraint = Constraint(f"CageConstraint_{cell_pos}", scope_vars)

        # Check function that enforces the target arithmetic for each possible operator
        def check_cage_tuple(tup):
            op_str   = tup[0]
            cell_vals = tup[1:]  # integer values for each cell

            if op_str == '+':
                return sum(cell_vals) == target
            elif op_str == '*':
                return prod(cell_vals) == target
            elif op_str == '-':
                # Only valid for two cells
                if len(cell_vals) != 2:
                    return False
                return abs(cell_vals[0] - cell_vals[1]) == target
            elif op_str == '/':
                # Only valid for two cells
                if len(cell_vals) != 2:
                    return False
                bigger, smaller = max(cell_vals), min(cell_vals)
                return (bigger % smaller == 0) and (bigger // smaller == target)

        # Gather all valid tuples that satisfy the cage constraint
        all_domains = [cage_var.domain()] + [cv.domain() for cv in cage_cells]
        satisfying_tuples = []
        for combo in product(*all_domains):
            if check_cage_tuple(combo):
                satisfying_tuples.append(combo)

        constraint.add_satisfying_tuples(satisfying_tuples)
        csp.add_constraint(constraint)

    # Combine the cell variables with any new cage variables, to return them all
    all_vars = [v for row in var_matrix for v in row]
    for v in csp.vars:
        if v not in all_vars:
            all_vars.append(v)

    return csp, all_vars






        
        
        
        
    

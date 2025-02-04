# =============================
# Student Names: Corey McCann
# Group ID: 43
# Date: 01/28/2025
# =============================
# CISC 352 - W23
# heuristics.py
# desc:
#


#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete problem solution.

'''This file will contain different constraint propagators to be used within
   the propagators

1. ord_dh (worth 0.25/3 points)
    - a Variable ordering heuristic that chooses the next Variable to be assigned 
      according to the Degree heuristic

2. ord_mv (worth 0.25/3 points)
    - a Variable ordering heuristic that chooses the next Variable to be assigned 
      according to the Minimum-Remaining-Value heuristic


var_ordering == a function with the following template
    var_ordering(csp)
        ==> returns Variable

    csp is a CSP object---the heuristic can use this to get access to the
    Variables and constraints of the problem. The assigned Variables can be
    accessed via methods, the values assigned can also be accessed.

    var_ordering returns the next Variable to be assigned, as per the definition
    of the heuristic it implements.
   '''

def ord_dh(csp):
    ''' return next Variable to be assigned according to the Degree Heuristic '''
    unassigned_vars = csp.get_all_unasgn_vars()
    highest_degree_var = unassigned_vars[0]
    highest_degree = len(csp.get_cons_with_var(unassigned_vars[0]))
    
    for var in unassigned_vars:
        degree = len(csp.get_cons_with_var(var))
        if degree > highest_degree:
            highest_degree_var = var
            highest_degree = degree
            
    return highest_degree_var


def ord_mrv(csp):
    ''' return Variable to be assigned according to the Minimum Remaining Values heuristic '''
    unassigned_vars = csp.get_all_unasgn_vars()
    min_vals_var = unassigned_vars[0]
    min_vals = len(unassigned_vars[0].cur_domain())
    
    for var in unassigned_vars:
        num_vals = len(var.cur_domain())
        if num_vals < min_vals:
            min_vals_var = var
            min_vals = num_vals
            
    return min_vals_var
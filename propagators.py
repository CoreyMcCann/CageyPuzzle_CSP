# =============================
# Student Names: Corey McCann
# Group ID: 43
# Date: 01/28/2025
# =============================
# CISC 352 - W23
# propagators.py
# desc:
#


#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete problem solution.

from collections import deque

'''This file will contain different constraint propagators to be used within
   bt_search.

    1. prop_FC (worth 0.5/3 marks)
        - a propagator function that propagates according to the FC algorithm that 
          check constraints that have exactly one Variable in their scope that has 
          not assigned with a value, and prune appropriately

    2. prop_GAC (worth 0.5/3 marks)
        - a propagator function that propagates according to the GAC algorithm, as 
          covered in lecture

   propagator == a function with the following template
      propagator(csp, newly_instantiated_variable=None)
           ==> returns (True/False, [(Variable, Value), (Variable, Value) ...]

      csp is a CSP object---the propagator can use this to get access
      to the variables and constraints of the problem. The assigned Variables
      can be accessed via methods, the values assigned can also be accessed.

      newly_instaniated_variable is an optional argument.
      if newly_instantiated_variable is not None:
          then newly_instantiated_variable is the most
           recently assigned Variable of the search.
      else:
          progator is called before any assignments are made
          in which case it must decide what processing to do
           prior to any Variables being assigned. SEE BELOW

       The propagator returns True/False and a list of (Variable, Value) pairs.
       Return is False if a deadend has been detected by the propagator.
       in this case bt_search will backtrack
       return is true if we can continue.

      The list of Variable values pairs are all of the values
      the propagator pruned (using the Variable's prune_value method).
      bt_search NEEDS to know this in order to correctly restore these
      values when it undoes a Variable assignment.

      NOTE propagator SHOULD NOT prune a value that has already been
      pruned! Nor should it prune a value twice

      PROPAGATOR called with newly_instantiated_variable = None
      PROCESSING REQUIRED:
        for plain backtracking (where we only check fully instantiated
        constraints)
        we do nothing...return true, []

        for forward checking (where we only check constraints with one
        remaining Variable)
        we look for unary constraints of the csp (constraints whose scope
        contains only one Variable) and we forward_check these constraints.

        for gac we establish initial GAC by initializing the GAC queue
        with all constaints of the csp


      PROPAGATOR called with newly_instantiated_variable = a Variable V
      PROCESSING REQUIRED:
         for plain backtracking we check all constraints with V (see csp method
         get_cons_with_var) that are fully assigned.

         for forward checking we forward check all constraints with V
         that have one unassigned Variable left

         for gac we initialize the GAC queue with all constraints containing V.
   '''

def prop_BT(csp, newVar=None):
    '''Do plain backtracking propagation. That is, do no
    propagation at all. Just check fully instantiated constraints'''

    if not newVar:
        return True, []
    for c in csp.get_cons_with_var(newVar):
        if c.get_n_unasgn() == 0:
            vals = []
            vars = c.get_scope()
            for var in vars:
                vals.append(var.get_assigned_value())
            if not c.check_tuple(vals):
                return False, []
    return True, []


def prop_FC(csp, newVar=None):
    '''Do forward checking. That is check constraints with
       only one uninstantiated Variable. Remember to keep
       track of all pruned Variable,value pairs and return '''
    pruned_values = []
    
    # get all constraints in the csp that include newVar in its scope
    if not newVar:
        constraints = csp.get_all_cons()
    else:
        constraints = csp.get_cons_with_var(newVar)
    
    for constraint in constraints:
        # looking for constraints with only one unassigned variable
        if constraint.get_n_unasgn() == 1:
            unassigned_var = constraint.get_unasgn_vars()[0]
            
            # loop through all the values in the unassigned variables current domain
            for value in unassigned_var.cur_domain():
                # use check_var_val to see if we assign unassigned_var with value there are still satisfying tuples in this constraint
                if not constraint.check_var_val(unassigned_var, value):
                    # this only executes if the potential variable assignment does not satisfy the constraint, so we can prune this value
                    if unassigned_var.in_cur_domain(value):
                        unassigned_var.prune_value(value)
                        pruned_values.append((unassigned_var, value))
                           
            # if our current domain size is now zero this means we have pruned all values
            # and can't find a solution with that assignment    
            if unassigned_var.cur_domain_size() == 0:
                return False, pruned_values
            
    return True, pruned_values


def prop_GAC(csp, newVar=None):
    '''Do GAC propagation. If newVar is None we do initial GAC enforce
       processing all constraints. Otherwise we do GAC enforce with
       constraints containing newVar on GAC Queue'''
    if not newVar:
        constraints = csp.get_all_cons()
    else: 
        constraints = csp.get_cons_with_var(newVar)
    
    queue = deque(constraints)
    pruned_values = []

    while queue:
        cur_constraint = queue.pop()
        
        # loop through all variables in the current constraints scope
        for var in cur_constraint.get_scope():
            # loop through all values in the current variables domain
            for val in var.cur_domain():
                # use check_var_val to see if we assign var with val there are still satisfying tuples in this constraint
                if not cur_constraint.check_var_val(var, val):
                    # this only executes if the potential variable assignment does not satisfy the constraint, so we can prune this value
                    if var.in_cur_domain(val):
                        var.prune_value(val)
                        pruned_values.append((var, val))
                    
                    # now we must add all constraints to the queue that involve the variable that we just pruned
                    for constraint in csp.get_cons_with_var(var):
                        if constraint not in queue:
                            queue.appendleft(constraint)
                
            if var.cur_domain_size() == 0:
                return False, pruned_values  
            
    return True, pruned_values 


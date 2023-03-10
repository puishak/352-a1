# =============================
# Student Names: Absar, Shakib and Bigcanoe, Tanner
# Group ID: Group 29
# Date: 2023-02-05
# =============================
# CISC 352 - W23
# propagators.py
# desc: An implementation of the propogator functions for the cagey csp. The functions implemented are...
# the forward checking propogator, as well as the generalized arc consistency propogator.


#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete problem solution.

'''This file will contain different constraint propagators to be used within
   bt_search.

   propagator == a function with the following template
      propagator(csp, newly_instantiated_variable=None)
           ==> returns (True/False, [(Variable, Value), (Variable, Value) ...]

      csp is a CSP object---the propagator can use this to get access
      to the variables and constraints of the problem. The assigned variables
      can be accessed via methods, the values assigned can also be accessed.

      newly_instaniated_variable is an optional argument.
      if newly_instantiated_variable is not None:
          then newly_instantiated_variable is the most
           recently assigned variable of the search.
      else:
          progator is called before any assignments are made
          in which case it must decide what processing to do
           prior to any variables being assigned. SEE BELOW

       The propagator returns True/False and a list of (Variable, Value) pairs.
       Return is False if a deadend has been detected by the propagator.
       in this case bt_search will backtrack
       return is true if we can continue.

      The list of variable values pairs are all of the values
      the propagator pruned (using the variable's prune_value method).
      bt_search NEEDS to know this in order to correctly restore these
      values when it undoes a variable assignment.

      NOTE propagator SHOULD NOT prune a value that has already been
      pruned! Nor should it prune a value twice

      PROPAGATOR called with newly_instantiated_variable = None
      PROCESSING REQUIRED:
        for plain backtracking (where we only check fully instantiated
        constraints)
        we do nothing...return true, []

        for forward checking (where we only check constraints with one
        remaining variable)
        we look for unary constraints of the csp (constraints whose scope
        contains only one variable) and we forward_check these constraints.

        for gac we establish initial GAC by initializing the GAC queue
        with all constaints of the csp


      PROPAGATOR called with newly_instantiated_variable = a variable V
      PROCESSING REQUIRED:
         for plain backtracking we check all constraints with V (see csp method
         get_cons_with_var) that are fully assigned.

         for forward checking we forward check all constraints with V
         that have one unassigned variable left

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
       only one uninstantiated variable. Remember to keep
       track of all pruned variable,value pairs and return '''
      
    #If the newVar is true
    if (newVar):
        #constraints is set to the list of constraints that include newVar in their scope.
        constraints = csp.get_cons_with_var(newVar)
    else:
        #constraints is set to the list of all constraints in the csp.
        constraints = csp.get_all_cons()
    
    #constraint satisfaction is set to the list of constraints if the given constraints number of unassigned variables is one.
    constraintSatisfaction = [constraint for constraint in constraints if constraint.get_n_unasgn() == 1]
    
    #pruned is an empty list.
    pruned = []
    
    #for constraint in constraint satisfaction.
    for constraint in constraintSatisfaction:
        #variable is set to the given constraints unassigned variables at index zero.
        variable = constraint.get_unasgn_vars()[0]
    
        #for domain value in the current unassigned variable's current domain of values.
        for domainValue in variable.cur_domain():
        
            #If constraint does not have support in the unassigned variable in the current domain value.
            #and the pair of variable and domain value are not in the pruned list.
            if (not constraint.has_support(variable, domainValue)) and ((variable, domainValue) not in pruned):
            
                #Then the domain value is pruned (removed) from the current domain.
                variable.prune_value(domainValue)
            
                #The empty list pruned then appends the pair unassigned vairable and domain value.
                pruned.append((variable, domainValue))

        #if the unassigned variables current domain size is zero.
        if variable.cur_domain_size() == 0:
        
            #Then return false and pruned the list of unassigned variables and removed domain values pairs
            return False, pruned

    #return True and pruned the list of unassigned variables and removed domain values pairs
    return True, pruned


def prop_GAC(csp, newVar=None):
    '''Do GAC propagation. If newVar is None we do initial GAC enforce
       processing all constraints. Otherwise we do GAC enforce with
       constraints containing newVar on GAC Queue'''
    
    #If newVar is true
    if (newVar):
        #Then constraints is set to the csp's list of constraints that include newVar in their scope
        constraints = csp.get_cons_with_var(newVar)
    else:
        #otherwise the constraints are set to all of the constraints of the csp.
        constraints = csp.get_all_cons()

    #The generalized arc consistency queue data structure is initialized to hold the constraints
    #that need to be looked at again incase of violation.
    generalizedArcConsistencyQueue = []

    #For constraint in constraints
    for constraint in constraints:

        #Add the constraint to the queue.
        generalizedArcConsistencyQueue.append(constraint)

    #Create an empty array called pruned to hold the removed values from the domain.
    pruned = []

    #While the length of the queue is true.
    while len(generalizedArcConsistencyQueue):

        #constraint is set to the popped value of the queue.
        constraint = generalizedArcConsistencyQueue.pop(0)

        #For variable in the constraints scope.
        for variable in constraint.get_scope():
            #if the domain value is in the variables current domain.
            for domainValue in variable.cur_domain():

                #then if the constraint does not has a supporting tuple (a set of 
                #assignments satisfying the constraint where each value is still in the 
                #corresponding variables current domain.
                #And the pair is not currently in the pruned array.
                if (not constraint.has_support(variable, domainValue)) and ((variable, domainValue) not in pruned):

                    #then prune the domain value of the variable
                    variable.prune_value(domainValue)

                    #add the pair of variable and domain value to the pruned array
                    pruned.append((variable, domainValue))

                    #if the variables current domain size is zero
                    if variable.cur_domain_size() == 0:

                        #then we can clear the queue
                        generalizedArcConsistencyQueue.clear()

                        #and return False as well as the array of pruned pairs
                        return False, pruned
                    
                    #otherwise
                    else:

                        #for a C-Prime in the list of constraints that include variable in their scope
                        for cPrime in csp.get_cons_with_var(variable):

                            #if the C-Prime is not in the queue
                            if cPrime not in generalizedArcConsistencyQueue:

                                #then add the C-Prime value to the queue.
                                generalizedArcConsistencyQueue.append(cPrime)
    
    #return true as well as the array of pruned pairs
    return True, pruned

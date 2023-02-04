# =============================
# Student Names:
# Group ID:
# Date:
# =============================
# CISC 352 - W23
# heuristics.py
# desc:
#


#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete problem solution.

'''This file will contain different constraint propagators to be used within
   the propagators

var_ordering == a function with the following template
    var_ordering(csp)
        ==> returns Variable

    csp is a CSP object---the heuristic can use this to get access to the
    variables and constraints of the problem. The assigned variables can be
    accessed via methods, the values assigned can also be accessed.

    var_ordering returns the next Variable to be assigned, as per the definition
    of the heuristic it implements.
   '''

def ord_dh(csp):
   ''' return variables according to the Degree Heuristic '''

   #The maximum degree.
   maxDegree = -1

   #Create an empty variabe.
   variable = None
   
   #For i in the list of unassigned variables in the CSP.
   for i in csp.get_all_unasgn_vars():
      
      #Set the current degree to one.
      currentDegree = 0
      
      #For k in the list of constraints that include i in their scope. Where i is a variable in the list
      #of unassigned variables in the CSP.
      for k in csp.get_cons_with_var(i):
         
         #assignedVariables is equal to the list of unassigned variables in the constraint k.
         unassignedVariables = k.get_all_unasgn_vars()
         
         #vistedVars is equal to an empty list that will hold the visited variables.
         visitedVars = []
         
         #For an unassigned variable in the list of unassigned variables.
         for unassignedVariable in unassignedVariables:
            
            #If that unassigned variable is i (a number that corresponds to the number of unassigned variables
            #in the constraints scope) and that unassignedVariable is not is the list of visited variables.
            if (not unassignedVariable is i) and (unassignedVariable not in visitedVars):
               
               #Then add the variable to the list of visited variables.
               visitedVars.append(unassignedVariable)
               
               #Increase the current degree.
               currentDegree += 1
       
      #if the current degree is greater than the max degree of -1. 
      if currentDegree > maxDegree:
         
         #Then max degree is the current degree.
         maxDegree = currentDegree
         
         #And the variable is set to i.
         variable = i
     
   #return the variable.
   return variable
      
   
   

def ord_mrv(csp):
   ''' return variable according to the Minimum Remaining Values heuristic '''
   #The minimum remaining value is set to infinity. Has to be a large value to start.
   minimumRemainingValue = float('inf')
   
   #Create an empty variable.
   variable = None
    
   #For i in the list of all unassigned variables in the CSP.
   for i in csp.get_all_asgn_vars():
    
      #the remaining value is set to the current domain size (the size of the variables domain) of the
      #unassigned variable i.
      remainingValue = i.cur_domain_size()
    
      #If the remaining value is less than the minimum remaining value
      if remainingValue < minimumRemainingValue:
         
         #Then the minimum remaining value is set to the remaining value.
         minimumRemainingValue = remainingValue
         
         #The empty variable is set to the unassigned variable i.
         variable = i
     
   #return the variable
   return variable

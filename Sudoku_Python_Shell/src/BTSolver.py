import SudokuBoard
import Variable
import Domain
import Trail
import Constraint
import ConstraintNetwork
import time
import random

#my imports
import numpy as np

class BTSolver:

    # ==================================================================
    # Constructors
    # ==================================================================

    def __init__ ( self, gb, trail, val_sh, var_sh, cc ):
        self.network = ConstraintNetwork.ConstraintNetwork(gb)
        self.hassolution = False
        self.gameboard = gb
        self.trail = trail

        self.varHeuristics = var_sh
        self.valHeuristics = val_sh
        self.cChecks = cc

        #my mods
        self.initFCCheck = True
        self.initNORCheck = True
        self.assignedVar = None


    # ==================================================================
    # Consistency Checks
    # ==================================================================

    # Basic consistency check, no propagation done
    def assignmentsCheck ( self ):
        for c in self.network.getConstraints():
            if not c.isConsistent():
                return False
        return True

    """
        Part 1 TODO: Implement the Forward Checking Heuristic

        This function will do both Constraint Propagation and check
        the consistency of the network

        (1) If a variable is assigned then eliminate that value from
            the square's neighbors.

        Note: remember to trail.push variables before you assign them
        Return: a tuple of a dictionary and a bool. The dictionary contains all MODIFIED variables, mapped to their MODIFIED domain.
                The bool is true if assignment is consistent, false otherwise.
    """
    def forwardChecking ( self ):

        

        #save trail before constraint prop
        # self.trail.placeTrailMarker()

        RetDict = dict()
        # print("in fc")


        AllVarList = self.network.getVariables()


        if self.initFCCheck:
            self.initFCCheck = False

            for aVar in AllVarList:
                # print(aVar.isAssigned())
                if aVar.isAssigned():

                    # if self.assignedVar is None:
                    #     return ({},True)

                    #variable is assigned perf FC
                    AssignedVal = aVar.getAssignment()
                    # print("vAR" + str(aVar))

                    NeighborOfVar = self.network.getNeighborsOfVariable(aVar)
                    # print("neigh" + str(NeighborOfVar))

                    for aNeigh in NeighborOfVar:
                        # print("neigh " + str(aNeigh))
                        # print("val" + str(aNeigh.getValues()))

                        if AssignedVal in aNeigh.getValues():
                            
                            #check if neighbor is assigned
                            if aNeigh.isAssigned():
                                return (RetDict,False)

                            #trail push before assign
                            self.trail.push(aNeigh)

                            #remove the assignedval from the neighbor
                            aNeigh.removeValueFromDomain(AssignedVal)

                            RetDict[aNeigh] = aNeigh.getDomain()

                            if aNeigh.size() == 0:
                                #undo the trail
                                # self.trail.undo()

                                # print("false undo")

                                return (RetDict,False)
                            
        else:
            #not initial FCrun

            aVar = self.assignedVar

            #variable is assigned perf FC
            AssignedVal = aVar.getAssignment()
            # print("vAR" + str(aVar))

            NeighborOfVar = self.network.getNeighborsOfVariable(aVar)
            # print("neigh" + str(NeighborOfVar))

            for aNeigh in NeighborOfVar:
                # print("neigh " + str(aNeigh))
                # print("val" + str(aNeigh.getValues()))

                if AssignedVal in aNeigh.getValues():

                    #check if neighbor is assigned
                    if aNeigh.isAssigned():
                        return (RetDict,False)
                    
                    #check if the domain size is 1
                    if aNeigh.size() == 1:
                        return (RetDict,False)


                    #trail push before assign
                    self.trail.push(aNeigh)

                    #remove the assignedval from the neighbor
                    aNeigh.removeValueFromDomain(AssignedVal)

                    RetDict[aNeigh] = aNeigh.getDomain()

                    # if aNeigh.size() == 0:
                    #     #undo the trail
                    #     # self.trail.undo()

                    #     # print("false undo")

                    #     return (RetDict,False)
             


        return (RetDict,True)

    # =================================================================
	# Arc Consistency
	# =================================================================
    def arcConsistency( self ):
        assignedVars = []
        for c in self.network.constraints:
            for v in c.vars:
                if v.isAssigned():
                    assignedVars.append(v)
        while len(assignedVars) != 0:
            av = assignedVars.pop(0)
            for neighbor in self.network.getNeighborsOfVariable(av):
                if neighbor.isChangeable and not neighbor.isAssigned() and neighbor.getDomain().contains(av.getAssignment()):
                    neighbor.removeValueFromDomain(av.getAssignment())
                    if neighbor.domain.size() == 1:
                        neighbor.assignValue(neighbor.domain.values[0])
                        assignedVars.append(neighbor)

    
    """
        Part 2 TODO: Implement both of Norvig's Heuristics

        This function will do both Constraint Propagation and check
        the consistency of the network

        (1) If a variable is assigned then eliminate that value from
            the square's neighbors.

        (2) If a constraint has only one possible place for a value
            then put the value there.

        Note: remember to trail.push variables before you assign them
        Return: a pair of a dictionary and a bool. The dictionary contains all variables 
		        that were ASSIGNED during the whole NorvigCheck propagation, and mapped to the values that they were assigned.
                The bool is true if assignment is consistent, false otherwise.
    """

    def norvigCheck ( self ):
        # return ({}, False)

        # print("in norvig check")
        RetDict = dict()

        AllVarList = self.network.getVariables()

        if self.initNORCheck:
            self.initNORCheck = False

            #part 1 FC which is constrain prop
           

            for aVar in AllVarList:
                # print(aVar.isAssigned())
                if aVar.isAssigned():

                    # if self.assignedVar is None:
                    #     return ({},True)

                    #variable is assigned perf FC
                    AssignedVal = aVar.getAssignment()
                    # print("vAR" + str(aVar))

                    NeighborOfVar = self.network.getNeighborsOfVariable(aVar)
                    # print("neigh" + str(NeighborOfVar))

                    for aNeigh in NeighborOfVar:
                        # print("neigh " + str(aNeigh))
                        # print("val" + str(aNeigh.getValues()))

                        if AssignedVal in aNeigh.getValues():
                            
                            #check if neighbor is assigned
                            if aNeigh.isAssigned():
                                return (RetDict,False)
                            
                            if aNeigh.size() == 1:
                                    # print("Error in removing val one check")
                                    return (RetDict,False)

                            #trail push before assign
                            self.trail.push(aNeigh)

                            #remove the assignedval from the neighbor
                            aNeigh.removeValueFromDomain(AssignedVal)

                            RetDict[aNeigh] = aNeigh.getDomain()

                            # if aNeigh.size() == 0:
                            #     #undo the trail
                            #     # self.trail.undo()

                            #     # print("false undo")

                            #     return (RetDict,False)

        else:
            #not initial FCrun

            aVar = self.assignedVar

            #variable is assigned perf FC
            AssignedVal = aVar.getAssignment()
            # print("vAR" + str(aVar))

            NeighborOfVar = self.network.getNeighborsOfVariable(aVar)
            # print("neigh" + str(NeighborOfVar))

            for aNeigh in NeighborOfVar:
                # print("neigh " + str(aNeigh))
                # print("val" + str(aNeigh.getValues()))

                if AssignedVal in aNeigh.getValues():

                    #check if neighbor is assigned
                    if aNeigh.isAssigned():
                        return (RetDict,False)
                    
                    #check if the domain size is 1
                    if aNeigh.size() == 1:
                        return (RetDict,False)


                    #trail push before assign
                    self.trail.push(aNeigh)

                    #remove the assignedval from the neighbor
                    aNeigh.removeValueFromDomain(AssignedVal)

                    RetDict[aNeigh] = aNeigh.getDomain()

                    # if aNeigh.size() == 0:
                    #     #undo the trail
                    #     # self.trail.undo()

                    #     # print("false undo")

                    #     return (RetDict,False)

        
                        
        #part 2 if contraint has one possible value then assign it that
        

        #norvig v2
        TheN = self.gameboard.N
        # print(TheN)

        

        for aUnit in self.network.getConstraints():
            TheVarDomaincounter = np.zeros((TheN,), dtype=int)
            # print("Aunit " + str(aUnit))

            TheConstraintUnitVars = aUnit.vars


            # print("part 1")

            for aVariable in TheConstraintUnitVars:

                if aVariable.isAssigned() is False:
                
                    # print(aVariable)

                    for aValue in aVariable.getValues():
                        TheVarDomaincounter[aValue-1] += 1

            # print(TheVarDomaincounter)

            #second subpart
            # print("second subpart")

            TheNumArreqOne = np.where(TheVarDomaincounter == 1)[0]
            
            # print(np.where(TheVarDomaincounter == 1)[0])

            for aOneIndex in TheNumArreqOne:
                # print(aOneIndex)
                #find the domain in the var
                TarValue = int(aOneIndex) + 1

                for aVar in TheConstraintUnitVars:
                    if TarValue in aVar.getValues():
                        #found var and the val then assign it
                        #push before assign
                        self.trail.push(aVar)

                        #assign value to var
                        aVar.assignValue(TarValue)

                        RetDict[aVar] = aVar.getDomain()

                        #propagate changes

                        #variable is assigned perf FC
                        AssignedVal = TarValue
                        # print("vAR" + str(aVar))

                        NeighborOfVar = self.network.getNeighborsOfVariable(aVar)
                        # print("neigh" + str(NeighborOfVar))

                        for aNeigh in NeighborOfVar:
                            # print("neigh " + str(aNeigh))
                            # print("val" + str(aNeigh.getValues()))

                            if AssignedVal in aNeigh.getValues():

                                #check if neighbor is assigned
                                if aNeigh.isAssigned():
                                    # print("print error neigh is assigned")
                                    return (RetDict,False)
                                    # self.trail.undo()

                                if aNeigh.size() == 1:
                                    # print("Error in removing val one check")
                                    return (RetDict,False)
                                    # self.trail.undo()
                                


                                #trail push before assign
                                self.trail.push(aNeigh)

                                #remove the assignedval from the neighbor
                                aNeigh.removeValueFromDomain(AssignedVal)

                                RetDict[aNeigh] = aNeigh.getDomain()


        # print(self.network.isConsistent())
        return (RetDict,self.assignmentsCheck())




    """
         Optional TODO: Implement your own advanced Constraint Propagation

         Completing the three tourn heuristic will automatically enter
         your program into a tournament.
     """
    def getTournCC ( self ):
        return False

    # ==================================================================
    # Variable Selectors
    # ==================================================================

    # Basic variable selector, returns first unassigned variable
    def getfirstUnassignedVariable ( self ):
        for v in self.network.variables:
            if not v.isAssigned():
                return v

        # Everything is assigned
        return None

    """
        Part 1 TODO: Implement the Minimum Remaining Value Heuristic

        Return: The unassigned variable with the smallest domain
    """
    def getMRV ( self ):

        # print("in the mrv")
        AllVarList = self.network.getVariables()
        smallestDomainUnassignedVar = None
        smallestDomainSize = None #ask justin what to set the upper limit too.  None bro
        
        for aVar in AllVarList:

            if not aVar.isAssigned():

                aVarDomainSize = aVar.size()

                # print(f"testing var {aVar} {aVarDomainSize}")
                

                if (smallestDomainUnassignedVar is None) or (aVarDomainSize < smallestDomainSize):
                    # print("updating the smallest")
                    smallestDomainUnassignedVar = aVar
                    smallestDomainSize = aVarDomainSize

                

                
                            
        return smallestDomainUnassignedVar

    """
        Part 2 TODO: Implement the Minimum Remaining Value Heuristic
                       with Degree Heuristic as a Tie Breaker

        Return: The unassigned variable with the smallest domain and affecting the  most unassigned neighbors.
                If there are multiple variables that have the same smallest domain with the same number of unassigned neighbors, add them to the list of Variables.
                If there is only one variable, return the list of size 1 containing that variable.
    """
    def MRVwithTieBreaker ( self ):
        return None

    """
         Optional TODO: Implement your own advanced Variable Heuristic

         Completing the three tourn heuristic will automatically enter
         your program into a tournament.
     """
    def getTournVar ( self ):
        return None

    # ==================================================================
    # Value Selectors
    # ==================================================================

    # Default Value Ordering
    def getValuesInOrder ( self, v ):
        values = v.domain.values
        return sorted( values )

    """
        Part 1 TODO: Implement the Least Constraining Value Heuristic

        The Least constraining value is the one that will knock the least
        values out of it's neighbors domain.

        Return: A list of v's domain sorted by the LCV heuristic
                The LCV is first and the MCV is last
    """
    def getValuesLCVOrder ( self, v ):
        # print("In LCV")

        ValueNeighNumAppearDict = dict()

        # print(f" v values {v.getValues()}")

        #initialize dict

        for aDomainVal in v.getValues():
            ValueNeighNumAppearDict[aDomainVal] = 0

        # print(ValueNeighNumAppearDict)

        #for each neighbor get val

        for aNeighVar in self.network.getNeighborsOfVariable(v):
            if not aNeighVar.isAssigned():
                

                NeighDomainValues = aNeighVar.getValues()

                # print(f"neighbor val {NeighDomainValues}")


                if len(ValueNeighNumAppearDict) < len(NeighDomainValues):
                    InnerForIter = ValueNeighNumAppearDict.keys()

                    for aKeyinVNNDict in InnerForIter:
                        # print(f"checking {aKeyinVNNDict}")

                        if aKeyinVNNDict in NeighDomainValues:
                            #addd 1
                            ValueNeighNumAppearDict[aKeyinVNNDict] += 1

                else:
                    #case 2
                    InnerForIter = NeighDomainValues

                    for aKeyNeighDomain in InnerForIter:
                        # print(f"checking2 {aKeyNeighDomain}")

                        if aKeyNeighDomain in ValueNeighNumAppearDict:
                            #addd 1
                            ValueNeighNumAppearDict[aKeyNeighDomain] += 1

        # print(ValueNeighNumAppearDict)

       

        # print("test sort")
        ReturnLCVMinToMaxList = [aval[0] for aval in sorted(ValueNeighNumAppearDict.items(), key=lambda x: (x[1],x[0]))]
        # print(ReturnLCVMinToMaxList)

       



        return ReturnLCVMinToMaxList

    """
         Optional TODO: Implement your own advanced Value Heuristic

         Completing the three tourn heuristic will automatically enter
         your program into a tournament.
     """
    def getTournVal ( self, v ):
        return None

    # ==================================================================
    # Engine Functions
    # ==================================================================

    def solve ( self, time_left=600):
        if time_left <= 60:
            return -1

        start_time = time.time()
        if self.hassolution:
            return 0

        # Variable Selection
        v = self.selectNextVariable()

        

        # check if the assigment is complete
        if ( v == None ):
            # Success
            self.hassolution = True
            return 0
        
        

        # Attempt to assign a value
        for i in self.getNextValues( v ):

            # Store place in trail and push variable's state on trail
            self.trail.placeTrailMarker()
            self.trail.push( v )


            # Assign the value
            v.assignValue( i )

            #store the assigned var in instance var
            self.assignedVar = v

            


            # Propagate constraints, check consistency, recur
            if self.checkConsistency():
                elapsed_time = time.time() - start_time 
                new_start_time = time_left - elapsed_time
                if self.solve(time_left=new_start_time) == -1:
                    return -1
                
            # If this assignment succeeded, return
            if self.hassolution:
                return 0

            # Otherwise backtrack
            self.trail.undo()
        
        return 0

    def checkConsistency ( self ):
        if self.cChecks == "forwardChecking":
            return self.forwardChecking()[1]

        if self.cChecks == "norvigCheck":
            return self.norvigCheck()[1]

        if self.cChecks == "tournCC":
            return self.getTournCC()

        else:
            return self.assignmentsCheck()

    def selectNextVariable ( self ):
        if self.varHeuristics == "MinimumRemainingValue":
            return self.getMRV()

        if self.varHeuristics == "MRVwithTieBreaker":
            return self.MRVwithTieBreaker()[0]

        if self.varHeuristics == "tournVar":
            return self.getTournVar()

        else:
            return self.getfirstUnassignedVariable()

    def getNextValues ( self, v ):
        if self.valHeuristics == "LeastConstrainingValue":
            return self.getValuesLCVOrder( v )

        if self.valHeuristics == "tournVal":
            return self.getTournVal( v )

        else:
            return self.getValuesInOrder( v )

    def getSolution ( self ):
        return self.network.toSudokuBoard(self.gameboard.p, self.gameboard.q)

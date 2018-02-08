# This file is part of the udkm1Dsimpy module.
#
# udkm1Dsimpy is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.
#
# Copyright (C) 2017 Daniel Schick

import more_itertools
class structure(object):
    
    
    """structure
    The structure class can hold various substructures. Each substructure can be either a layer of N unitCell 
    objects or a structure by itself. Thus it is possible to recursively build up 1D structures.
    """
    
    def __init__(self, name, **kwargs):
        """
        Properties (SetAccess=public,GetAccess=public)
        name                % STRING name of sample
        substructures = []; % CELL ARRAY of structures in sample
        substrate           % OBJECT HANDLE structure of the substrate
        numSubSystems = 1;  % INTEGER number of subsystems for heat and phonons (electronic, lattice, spins, ...) 
        """
        self.name          =  name
        self.numSubSystems =  1
        self.substructures  = []
        self.substrate     =  []
        
        
    def isnot_empty(self,any_structure):
        
        """Check whether a structure is empty or not"""
        
        if any_structure:
            return 1
        
    
    def addSubStructure(self,subStructure,N):
        
        """Add a substructure of N unitCells or N structures to the structure."""
        
        #check of the substructure is an instance of the unitCell of structure class
        
        if not (isinstance(subStructure,unitCell) or isinstance(subStructure,structure)):
            raise ValueError('Class '+type(subStructure).__name__+' is no possible sub structure.Only unitCell and structure classes are allowed!')
        pass
    
        # if a structure is added as a substructure, the substructure can not have a substrate!   
        
        if isinstance(subStructure,structure):
            if(self.isnot_empty(subStructure.substrate)):
                raise ValueError('No substrate in substructure allowed!')
                
        # check the number of subsystems of the substructure   
            
        if ((self.numSubSystems>1) and not(subStructure.numSubSystems == self.numSubSystems)):
            raise ValueError('The number of subsystems in each substructure must be the same!')
        else:
            self.numSubSystems = subStructure.numSubSystems
        
        
        self.substructures.append([subStructure, N])
        # add a substructure of N repetitions to the structure with
        #null = []
        #for i in range(N):
            #null.append(subStructure) 
        #self.substructures.append(null) 
    
    def addSubstrate(self,subStructure):
        if not isinstance(subStructure,structure):
            raise ValueError('Class '+type(subStructure).__name__+' is no possible substrate. Only structure class is allowed!')
            
        self.substrate = subStructure
    
    def getNumberOfSubStructures(self):
        N = 0
        for i in range(len(self.substructures)):
            if isinstance(self.substructures[i][0],unitCell):
                N = N + 1
        
            else:
                N = N + self.substructures[i][0].getNumberOfSubStructures()
        return N  
    
    def getNumberOfUnitCells(self):
        N = 0
        for i in range(len(self.substructures)):
            if isinstance(self.substructures[i][0],unitCell):
                N = N + self.substructures[i][1]
            else:
                N = N + self.substructures[i][0].getNumberOfUnitCells()*self.substructures[i][1]
                    
        return N  
    
    
    def getNumberOfUniqueUnitCells(self):
        N = len(self.getUniqueUnitCells()[0])
        return N
    
    
    def getUniqueUnitCells(self):
        newList   = []
        newListID = []
        for i in range(len(self.substructures)):
            if isinstance(self.substructures[i][0],unitCell):
                if self.substructures[i][0] not in newList:
                    newList   = newList   + [self.substructures[i][0]]
                    newListID = newListID + [self.substructures[i][0].ID]
            else:
                (newListID, newList) = self.substructures[i][0].getUniqueUnitCells()
        #print(newListID)        
        return newListID,newList
    
    def getUnitCellVectors(self):
        Index     =  []
        newList   =  []
        newListID =  []
        for j in range(len(self.substructures)):
            if isinstance(self.substructures[j][0],unitCell):
                Index     = Index     + [i for i, v in enumerate(self.getUniqueUnitCells()[1]) if v == self.substructures[j][0]]*self.substructures[j][1]
                newList   = newList   + [v for i, v in enumerate(self.getUniqueUnitCells()[1]) if v == self.substructures[j][0]]*self.substructures[j][1]
                newListID = newListID + [v.ID for i, v in enumerate(self.getUniqueUnitCells()[1]) if v == self.substructures[j][0]]*self.substructures[j][1]
            else:
                Index      = Index     + [self.substructures[j][0].getUnitCellVectors()[0]]*self.substructures[j][1]
                newList    = newList   + [self.substructures[j][0].getUnitCellVectors()[1]]*self.substructures[j][1]
                newListID  = newListID + [self.substructures[j][0].getUnitCellVectors()[2]]*self.substructures[j][1]
        return list(more_itertools.collapse(Index)),list(more_itertools.collapse(newList)),list(more_itertools.collapse(newListID))   

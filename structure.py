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
        
        # add a substructure of N repetitions to the structure with
        
        for i in range(N):
            self.substructures.append(subStructure)  

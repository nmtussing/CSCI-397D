""" 
Author: Nicholas Tussing 
islands.py
Creating the island class for island objects 
"""

class islands:
    def __init__(self):
        self.number = 0
        self.treasure = False
        self.terminal = False
        
    def hasTreasure(self):
        if self.treasure == True:
            return True
        else:   
            return False
        
    def isTerminal(self):
        if self.terminal == True:
            return True
        else:
            return False
        

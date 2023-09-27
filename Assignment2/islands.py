""" 
Author: Nicholas Tussing 
islands.py
Creating the island class for island objects 
"""
import agent

class islands:
    def __init__(self):
        self.location = 0
        self.treasure = False
        self.terminal = False
        self.name = ""

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
        
   

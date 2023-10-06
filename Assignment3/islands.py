""" 
Author: Nicholas Tussing 
islands.py
Creating the island class for island objects 
"""
import agent

class islands:
    def __init__(self, location, treasure, terminal, name, value):
        self.location = location
        self.treasure = treasure
        self.terminal = terminal
        self.name = name
        self.value = value

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
        
   

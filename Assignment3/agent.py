""" 
Author: Nicholas Tussing
agent.py
Creating a class for the agent object which will serve as the bot
traversing the environment
"""
import islands
class agent:
    def __init__(self) :
        self.reward = 0.0
        self.location = 1
        self.action = None
        self.treasureFound = 0
        self.islandsTraversed = 0
    
 
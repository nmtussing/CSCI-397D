"""
Assignment2.py
Author: Nicholas Tussing
Program to run the MDP with 10 states, truncated to 25 steps
"""
import  agent
import islands  
# Creating the environment 
island1 = islands.islands()
island1.number = 1
island2 = islands.islands()
island2.number = 2
island3 = islands.islands()
island3.number = 3
island3.treasure = True
island4 = islands.islands()
island4.number = 4
island5 = islands.islands()
island5.number = 5
island6 = islands.islands()
island6.number = 6
island6.treasure = True
island7 = islands.islands()
island7.number = 7
island8 = islands.islands()
island8.number = 8
island9 = islands.islands()
island9.number = 9
island9.treasure = True
island10 = islands.islands()
island10.number = 10

actionset = ['dig','moveNext']
#Creating instance of the probability matrix where the first column is the island number
#and second column is the probability to dig, and the remaining columns are the probability to 
#move to the other islands
probabilityMatrix = [
    [1, 0.1, 0, 0.9, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 0.1, 0, 0, 0.9, 0, 0, 0, 0, 0, 0, 0],
    [3, 0.1, 0, 0, 0, 0.45, 0, 0, 0, 0, 0, 0.45],
    [4, 0.1, 0, 0, 0, 0, 0.45, 0, 0, 0, 0, 0.45],
    [5, 0.1, 0, 0, 0, 0, 0, 0.9, 0, 0, 0, 0],
    [6, 0.1, 0, 0, 0, 0, 0, 0, 0.45, 0, 0, 0.45],
    [7, 0.1, 0, 0, 0, 0, 0, 0, 0, 0.90, 0, 0],
    [8, 0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0.45, 0.45],
    [9, 0.1, 0.45, 0, 0, 0, 0, 0, 0, 0, 0, 0.45],
    ]

if __name__ == "__main__":
    agent1 = agent.agent()
    print(agent1.location)
    agent1.location = 10
    print(agent1.location)
    print(island6.hasTreasure())
    value = probabilityMatrix
    print(probabilityMatrix[5][0])
    
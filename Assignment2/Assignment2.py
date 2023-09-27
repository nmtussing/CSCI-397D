"""
Assignment2.py
Author: Nicholas Tussing
Program to run the MDP with 10 states, truncated to 25 steps
"""
import random
import  agent
import islands  
# Creating the environment 
island1 = islands.islands()
island1.location = 1
island2 = islands.islands()
island2.location = 2
island3 = islands.islands()
island3.location = 3
island3.treasure = True
island4 = islands.islands()
island4.location = 4
island5 = islands.islands()
island5.location = 5
island6 = islands.islands()
island6.location = 6
island6.treasure = True
island7 = islands.islands()
island7.location = 7
island8 = islands.islands()
island8.location = 8
island9 = islands.islands()
island9.location = 9
island9.treasure = True
island10 = islands.islands()
island10.location = 10
island10.isTerminal = True

moves = ["dig", island1, island2, island3, island4, island5, island6, island7, island8, island9, island10]
#Creating instance of the probability matrix where the first column is the island number
#and second column is the probability to dig, and the remaining columns are the probability to 
#move to the other islands
probabilityMatrix = [
    [0.1, 0, 0.9, 0, 0, 0, 0, 0, 0, 0, 0],
    [0.1, 0, 0, 0.9, 0, 0, 0, 0, 0, 0, 0],
    [0.1, 0, 0, 0, 0.45, 0, 0, 0, 0, 0, 0.45],
    [0.1, 0, 0, 0, 0, 0.45, 0, 0, 0, 0, 0.45],
    [0.1, 0, 0, 0, 0, 0, 0.9, 0, 0, 0, 0],
    [0.1, 0, 0, 0, 0, 0, 0, 0.45, 0, 0, 0.45],
    [0.1, 0, 0, 0, 0, 0, 0, 0, 0.90, 0, 0],
    [0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0.45, 0.45],
    [0.1, 0.45, 0, 0, 0, 0, 0, 0, 0, 0, 0.45],
    ]

# Dig helper function
def dig(bot, island):
    if island.hasTreasure() == True:
        island.treasure = False
        bot.reward += 10
        bot.treasureFound += 1
        return True
    if island.hasTreasure():
        return False

# Function to run the simulation based on desired steps 
def runGame(steps):
    actions = []
    mainAgent = agent.agent()
    currentIsland = island1
    for i in range(steps):
        #choice = random.uniform(0.0,1.0)
        if currentIsland == island10:
            actions.append("Terminal state")
            return actions
        currentProbabilities =  probabilityMatrix[testAgent.location-1]
        nextMove = random.choices(moves, currentProbabilities)[0]
        actions.append(nextMove)
        if nextMove == "dig":
            dig(mainAgent,currentIsland)
        else:
            currentIsland = nextMove
            actions.append(f"Moved to {currentIsland}")
    return actions
            
                       
        

if __name__ == "__main__":  
   
    testAgent =  agent.agent()
    island100 = islands.islands()
    island100.name = "island100"
    currentIs = island100
    # Use random.choices() to select an element based on probabilities
    testAgent1 = agent.agent()
    currentProbabilities =  probabilityMatrix[testAgent1.location-1]
    print(currentProbabilities)
    n = random.choices(moves, currentProbabilities)[0]
    a = []
    a.append(f"Moved to {island100.name}")
    
    print(n)
    print(a)
    
    runGame(25)
    
   
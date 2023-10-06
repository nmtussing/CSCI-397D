"""
Assignment2.py
Author: Nicholas Tussing
Program to run the MDP with 10 states, truncated to 25 steps,
through 10 episodes.
"""
import random
import  agent
import islands  

        
    
# Creating the environment 
island1 = islands.islands(1,False,False,"island1",4)
island2 = islands.islands(2,False,False,"island2",5)
island3 = islands.islands(3,True,False,"island3", 6)
island4 = islands.islands(4,False,False,"island4", 7)
island5 = islands.islands(5,False,False,"island5", 8)
island6 = islands.islands(6,True,False,"island6",6)
island7 = islands.islands(7,False,False, "island7",7)
island8 = islands.islands(8, False,False,"island8",6)
island9 = islands.islands(9, True,False,"island9",5)
island10 = islands.islands(10, False,True,"island10",15)

islandArray = [ island1, island2, island3, island4, island5, island6, island7, island8, island9, island10]
#Creating instance of the probability matrix where the first column is the island number
#and second column is the probability to dig, and the remaining columns are the probability to 
#move to the other islands
probabilityMatrix = [
    [ 0, 0.9, 0, 0, 0, 0, 0, 0, 0, 0],
    [ 0, 0, 0.9, 0, 0, 0, 0, 0, 0, 0],
    [ 0, 0, 0, 0.45, 0, 0, 0, 0, 0, 0.45],
    [ 0, 0, 0, 0, 0.45, 0, 0, 0, 0, 0.45],
    [ 0, 0, 0, 0, 0, 0.9, 0, 0, 0, 0],
    [ 0, 0, 0, 0, 0, 0, 0.45, 0, 0, 0.45],
    [ 0, 0, 0, 0, 0, 0, 0, 0.90, 0, 0],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0.45, 0.45],
    [ 0.45, 0, 0, 0, 0, 0, 0, 0, 0, 0.45],
    ]

# Dig helper function
def dig(bot, island):
    if island.hasTreasure() == True:
        island.treasure = False
        #bot.reward += 2
        bot.treasureFound += 1
        return True
    if island.hasTreasure():
        return False

# Function for conducting the episodes 
def runEpisode(steps, gamma, episodes):
    for i in range(1,episodes+1):
        print(f"Episode {i}:")
        print(runGame(steps,gamma))
        
# Iterative value function for each state
def valueFinder(islands, gamma):
    islandValues = []
    
    for island in islands:
        steps = 0
        islandVal = 0
        nextIsland = None
        currentProbabilities =  probabilityMatrix[island.location-2]
        for prob in currentProbabilities:
            if prob > 0:
                index = currentProbabilities.index(prob)
                nextIsland = islandArray[index]
                islandVal += prob*nextIsland.value*gamma**steps
        islandValues.append(f"{island.name} value = {islandVal}")
    return islandValues
        


# Function to run the simulation based on desired steps 
def runGame(steps, gamma):
     
    actionsTaken = []
    agentMain = agent.agent() 
    agentMain.location = 1 
    currentLocation = island1
    
    for i in range(steps):
        if agentMain.location == 10:
            agentMain.reward += 5*gamma**i
            if agentMain.treasureFound == 3:
                agentMain.reward += 15*gamma**i
            actionsTaken.append(f"Step {i} & Final Reward: Reached Terminal Island & {agentMain.reward}")
            print(actionsTaken)
            return "Agent's cumulative reward " + str(agentMain.reward)
            
        currentProbabilities =  probabilityMatrix[agentMain.location-1]
        nextMove = random.choices(islandArray, currentProbabilities)[0]
        '''if nextMove == "dig":
            if currentLocation.hasTreasure == True:
                agentMain.reward += 15*gamma**i
            
            dig(agentMain,currentLocation)
            actionsTaken.append(f"Step {i} Action & Reward: dig & {agentMain.reward}")'''
        
        currentLocation = nextMove
        agentMain.location = currentLocation.location 
        if agentMain.islandsTraversed == 3:
            agentMain.reward += 2
        if agentMain.islandsTraversed == 6:
            agentMain.reward += -1
        agentMain.reward -= 1*gamma**i
        actionsTaken.append(f"Step {i} Action & Reward: Moved to {currentLocation.name} & {agentMain.reward}")
    print(actionsTaken)
    return "Agent's cumulative reward " + str(agentMain.reward)

            

if __name__ == "__main__":  

    print(runGame(25, .9))
    print(runEpisode(25,.9,10))
    print("State value for each island ->", valueFinder(islandArray,.9))
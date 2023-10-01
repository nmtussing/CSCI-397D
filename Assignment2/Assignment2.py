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
island1 = islands.islands()
island1.location = 1
island1.name = "island1"
island2 = islands.islands()
island2.location = 2
island2.name = "island2"
island3 = islands.islands()
island3.location = 3
island3.name = "island3"
island3.treasure = True
island4 = islands.islands()
island4.location = 4
island4.name = "island4"
island5 = islands.islands()
island5.location = 5
island5.name = "island5"
island6 = islands.islands()
island6.location = 6
island6.name = "island6"
island6.treasure = True
island7 = islands.islands()
island7.location = 7
island7.name = "island7"
island8 = islands.islands()
island8.location = 8
island8.name = "island8"
island9 = islands.islands()
island9.location = 9
island9.name = "island9"
island9.treasure = True
island10 = islands.islands()
island10.location = 10
island10.name = "island10"
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


# Function to run the simulation based on desired steps 
def runGame(steps, gamma):
     
    actionsTaken = []
    agentMain = agent.agent() 
    agentMain.location = 1 
    currentLocation = island1
    
    for i in range(1,steps+1):
        if agentMain.location == 10:
            agentMain.reward += 5*gamma**i
            if agentMain.treasureFound == 3:
                agentMain.reward += 15*gamma**i
            actionsTaken.append(f"Step {i} & Final Reward: Reached Terminal Island & {agentMain.reward}")
            return actionsTaken
            
        currentProbabilities =  probabilityMatrix[agentMain.location-1]
        nextMove = random.choices(moves, currentProbabilities)[0]
        if nextMove == "dig":
            if currentLocation.hasTreasure == True:
                agentMain.reward += 15*gamma**i
            
            dig(agentMain,currentLocation)
            actionsTaken.append(f"Step {i} Action & Reward: dig & {agentMain.reward}")
        else:
            currentLocation = nextMove
            agentMain.location = currentLocation.location 
            agentMain.reward -= 1*gamma**i
            actionsTaken.append(f"Step {i} Action & Reward: Moved to {currentLocation.name} & {agentMain.reward}")
    print(actionsTaken)
    return agentMain.reward

            

if __name__ == "__main__":  

    print(runGame(25, .9))
    print(runEpisode(25,.9,10))

    
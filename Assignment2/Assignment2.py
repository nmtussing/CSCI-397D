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

actionset = ['dig','moveNext']
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

def dig(bot, island):
    if island.hasTreasure() == True:
        island.treasure = False
        bot.reward += 10
        bot.treasureFound += 1
        return True
    if island.hasTreasure():
        return False

def runGame(steps):
    actions = []
    agent2 = agent.agent()
    agent2.location = 1
    currentIsland = 1
    for i in range(steps):
        choice = random.uniform(0.0,1.0)
        if agent2.location == 10:
            return actions
        ch
        
        """if choice <= 0.1:
            dig(agent2, island1)
            actions.append("Dig")
        if choice > 0.1:
    
            
            for i in range (2,11):
                if probabilityMatrix[currentIsland][i] > 0 and probabilityMatrix[currentIsland][i] <= choice:
                    currentIsland = i-2
                    agent2.location = i-2
                    actions.append(f"Moved to island {currentIsland}")
                if probabilityMatrix[currentIsland][i] > 0 and probabilityMatrix[currentIsland][i] >= choice:
                    currentIsland = i-2  
                    agent2.location = i-2
                    actions.append(f"Moved to island {currentIsland}")"""
        if currentIsland == 10:
            actions.append("Terminal state")
            return actions
    return actions
            
                       
        

if __name__ == "__main__":  
    moves = ["dig", "Move-Isalnd1","Move-Isalnd2","Move-Isalnd3","Move-Isalnd4","Move-Isalnd5","Move-Isalnd6","Move-Isalnd7","Move-Isalnd8","Move-Isalnd9","Move-Isalnd10"]
    probabilities = [0.1, 0.2, 0.3, 0.2, 0.2]

    # Use random.choices() to select an element based on probabilities
    random_element = random.choices(elements, probabilities)[0]
    print(random_element)
    
   
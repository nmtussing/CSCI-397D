"""
Assignment2.py
Author: Nicholas Tussing
Program to run the MDP with 10 states, truncated to 25 steps
"""
import  agent
import islands  

if __name__ == "__main__":
    agent1 = agent.agent()
    print(agent1.location)
    agent1.location = 10
    print(agent1.location)
    
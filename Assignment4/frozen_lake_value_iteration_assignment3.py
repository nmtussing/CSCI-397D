import sys
import gymnasium as gym
import collections
import numpy as np


ENV_NAME = "FrozenLake-v1"
GAMMA = 0.9
TEST_EPISODES = 20
SEED = 42


class Agent:
    def __init__(self):
        # Define env
        self.env = self.create_env()
    
        # Define state
        self.state = None
        self.stateNum = self.env.observation_space
        self.actionNum = self.env.action_space

        # Define rewards
        self.rewards =  collections.defaultdict(lambda: collections.defaultdict(float)) 

        # Define transits
        self.transits = collections.defaultdict(lambda: collections.Counter())
        self.transitions = np.zeros((self.stateNum, self.actionNum, self.stateNum))
        # Define values
        self.values = np.zeros(self.stateNum)
        pass

    @staticmethod
    def create_env():
        # Return created environment
        return gym.make(ENV_NAME, is_slippery = True)
        pass

    def update_transits_rewards(self, state, action, new_state, reward):
        # Get the key, which is a state action pair
        key = (state, action)
        # update rewards which is accessed by key plus the new state
        self.rewards[key][new_state]+= reward
        # update transits count which is accessed by key and new_state
        self.transits[key][state]+= 1
        pass

    def play_n_random_steps(self, count):
        self.env.reset()
        # for loop that iterates count number of times

        for i in range(count):
    
            # get an action
            randAction = self.env.action_space.sample()

            # step through the environment
            observation, reward, done, info = self.env.step(randAction)

            # update the transits rewards
            self.update_transits_rewards(self.state, randAction, observation, reward)
            # update the state
            self.state = observation
            pass

    def print_value_table(self):
        # print the value table in a 2d matrix format
        count = 0
        table = ""
        for value in self.values:
            if count % 4 == 0:
                table += "\n"
            table += (" %.3f " % value)
            count+= 1
        print(table)
        pass

    def extract_policy(self):
        # Define policy as an empty list
        policy = []

        # for every state
        for i in range(self.stateNum):

            # select the action
            action = self.select_action(i)
            # append action to the policy
            policy.append(action)
        # return policy
        return policy
        pass

    def print_policy(self, policy):
        # define actions in NL
        actionSpace = {1: "Up", 2:"Down",3:"Left",4:"Right"}
        count = 0
        pol = ""
        for action in policy:
            if count % 4 ==0:
                pol += "\n"
            pol += (" {} ".format(actionSpace[action]))
        print(pol)
        # nested for loop to print the actions in 2d matrix format
        pass

    def calc_action_value(self, state, action):
        # get target counts which access transits by state, action
        targetCount = self.transits[(state,action)]

        # get the sum of all the counts
        sumCount = sum(targetCount.values())
        finalSum = 0
        # for each target state
        for targetState in targetCount:
            p = targetCount[targetState] / sumCount
            reward = self.rewards[(state,action)][targetState]
            finalSum += p * (reward + GAMMA * self.values[targetState])
            # calculate the proportion of reward plus gamma * value of the target state, then sum it all together. 
        # return that sum
        return finalSum
        pass

    def select_action(self, state):
        # define best action and best value
        bestAction = -sys.maxsize-1
        bestValue = -sys.maxsize-1
        # For action in the range of actions
        for action in self.actionNum:

            # calculate the action value
            actionValue = self.calc_action_value(state,action)

            # if best value is less than action value
            if bestValue < actionValue:
                # update best value and best action
                bestAction = action
                bestValue = actionValue
        # return best actiodef print_value_table(self):
        #print_value_table(self)
        return bestAction
        # print the value table in a 2d matrix format
        pass

    def play_episode(self, env):
        # define reward and state
        env.reset()
        reward = 0
        rewardFinal = 0
        state = 0
        count = 0
        # While loop
        while True:

            # select an action
            action = self.select_action(state)
            # take a step
            observation, r, done , info = env.step(action)

            # if state is multiple
            if state == observation:
                # update reward
                reward += r    
                # update count
                count += 1 
            # else
            else:

                # update reward
                reward += r
                # update count
                count+= 1
            # update total reward
            rewardFinal +=reward
            # get out if we're done
            if done:
                break
            # set state to new state
            state = observation
        # return total reward
        return rewardFinal
        pass

    def value_iteration(self):
        # for each state
        for state in self.stateNum:

            # set state_values equalt to a list of calc_action_value for every action
            state_values = [self.calc_action_value(state,j) for j in range(self.actionNum)]

        # set self values to the max state_values
            self.values[state]= max(state_values)         

        pass


if __name__ == "__main__":
    test_env = Agent.create_env()
    agent = Agent()

    iter_no = 0
    best_reward = 0
    while True:
        iter_no += 1
        agent.play_n_random_steps(100)
        agent.value_iteration()

        reward = sum([agent.play_episode(test_env)for _ in range(TEST_EPISODES)]) / TEST_EPISODES # sum of play episode for all 20 episodes / number of episodes
        
        if reward > best_reward:
            print("Best reward updated %.3f -> %.3f" % (best_reward, reward))
            best_reward = reward

        if reward > 0.80:
            print("Solved in %d iterations!" % iter_no)
            agent.print_value_table()
            policy = agent.extract_policy()
            agent.print_policy(policy)
            break
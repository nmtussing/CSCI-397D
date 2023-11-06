#!/usr/bin/env python3
import gym
import collections
from tensorboardX import SummaryWriter

ENV_NAME = "FrozenLake-v1"
GAMMA = 0.9
ALPHA = 0.2
TEST_EPISODES = 20


class Agent:
    def __init__(self):
        # Initialize the environment using gym.make with ENV_NAME
        self.environment = gym.make(ENV_NAME, is_slippery = False  , new_step_api = True)
        # Set the initial state by resetting the environment
        self.state = self.environment.reset()
        # Initialize a default dictionary named values for storing the Q-values
        self.values = collections.defaultdict(float)
        pass

    def sample_env(self):
        # Sample a random action from the environment's action space
        randAction = self.environment.action_space.sample()
        # Use the sampled action to take a step in the environment
        observation, reward, done, truncated, _ = self.environment.step(randAction)
        # If the episode ends, reset the environment and store the new state
        newState = self.state
        if done:
        
            self.state = self.environment.reset()
        else:
            self.state = observation
        # Return a tuple containing the old state, action, reward, and new state
        return (newState, randAction, reward, observation)
        pass

    def best_value_and_action(self, state):
        # Initialize variables best_value and best_action to None
        best_value = None
        best_action = None

        # Iterate over all possible actions in the environment's action space
        for action in range(self.environment.action_space.n):

        # Calculate the Q-value for each state-action pair
            value = self.values[(state, action)]
        # Update best_value and best_action based on the calculated Q-value
            #if best_value == None:
            #if best_value < value or best_value == None:
            if best_value == None or best_value < value:
                best_value = value
                best_action = action
        # Return best_value and best_action
        return (best_value , best_action)
        pass

    def value_update(self, state, action, reward, new_state):
        # Call the best_value_and_action function to get the best Q-value for the new state
        qValue, qAction = self.best_value_and_action(new_state)
    
        # Calculate the new Q-value using the reward, gamma, and best Q-value of the new state
        newQValue =  reward + GAMMA * qValue
        # Update the Q-value of the current state-action pair using alpha and the new Q-value
        self.values[(state, action)] += ALPHA * (newQValue - self.values[(state, action)])
        pass

    def play_episode(self, env):
        # Initialize a variable total_reward to 0.0
        total_reward = 0.0
        # Reset the environment and store the initial state
        state = env.reset()
        # Enter a loop that continues until the episode ends
        while True:
        # Call the best_value_and_action function to get the best action for the current state
            best_reward, best_action =   self.best_value_and_action(state)
        # Take a step in the environment using the best action and store the new state, reward, and done flag
            observation, reward, done, info = env.step(best_action)
        # Update total_reward using the received reward
            total_reward += reward
        # If the episode enzbreak from the loop
            if done:
                #False
                break
        # Otherwise, update the state using the new state
            else:
                state =observation
        # Return the total reward
        return total_reward
        pass

    def print_values(self):
        # Print the Q-values in a readable format
        # Hint: You can use nested loops to iterate over states and actions
        for state in range(self.environment.observation_space.n):
            for action in range(self.environment.action_space.n):
                print(f"State {state}, Action {action}: Q-value = {self.values[state, action]}")
        pass

    def print_policy(self):
        # Print the policy derived from the Q-values
        # Initialize an empty dictionary named policy
        policy = collections.defaultdict()
        # Iterate over all possible states in the environment
        for states in range(self.environment.observation_space.n):
        # Call the best_value_and_action function to get the best action for each state
            best_action = self.best_value_and_action(states)
        # Update the policy dictionary with the state-action pair
            policy[states] = best_action
        # Print the state and corresponding best action
            print(f"State: {states} | Best Action {best_action}")
        # Return the policy dictionary
        pass


if __name__ == "__main__":
    test_env = gym.make(ENV_NAME)
    agent = Agent()
    writer = SummaryWriter(comment="-q-learning")

    iter_no = 0
    best_reward = 0.0
    while True:
        iter_no += 1
        state, action, reward, new_state = agent.sample_env()
        agent.value_update(state, action, reward, new_state)

        cumulative_reward = 0.0
        for _ in range(TEST_EPISODES):
            cumulative_reward += agent.play_episode(test_env)
        cumulative_reward /= TEST_EPISODES
        writer.add_scalar("reward", cumulative_reward, iter_no)
        if cumulative_reward > best_reward:
            print("Best reward updated %.3f -> %.3f" % (best_reward, cumulative_reward))
            best_reward = cumulative_reward
        if cumulative_reward > 0.80:
            print("Solved in %d iterations!" % iter_no)
            break
    writer.close()

    # Print the Q-values and extract/print the policy
    agent.print_values()
    agent.print_policy()

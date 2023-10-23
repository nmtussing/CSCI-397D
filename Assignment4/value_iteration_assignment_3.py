import gym
import collections
import numpy as np

ENV_NAME = "FrozenLake-v1"
GAMMA = 0.9
TEST_EPISODES = 20
SEED = 42

class Agent:
    def __init__(self):
        self.env = self.create_env()
        self.state = self.env.reset()
        self.transits = collections.defaultdict(collections.Counter)
        self.rewards = collections.defaultdict(float)

    @staticmethod
    def create_env():
        return gym.make(ENV_NAME)

    def update_transits_rewards(self, state, action, new_state, reward):
        self.transits[state, action][new_state] += 1
        self.rewards[state, action, new_state] = reward

    def play_n_random_steps(self, count):
        for _ in range(count):
            action = self.env.action_space.sample()
            new_state, reward, is_done, _ = self.env.step(action)
            self.update_transits_rewards(self.state, action, new_state, reward)
            self.state = self.env.reset() if is_done else new_state

    def calc_action_value(self, state, action):
        total_transitions = sum(self.transits[state, action].values())
        action_value = 0

        for new_state, count in self.transits[state, action].items():
            reward = self.rewards[state, action, new_state]
            action_value += (count / total_transitions) * (reward + GAMMA * self.value_table[new_state])

        return action_value

    def select_action(self, state):
        action_values = [self.calc_action_value(state, action) for action in range(self.env.action_space.n]
        return np.argmax(action_values)

    def play_episode(self, env):
        total_reward = 0
        state = env.reset()
        
        while True:
            action = self.select_action(state)
            new_state, reward, is_done, _ = env.step(action)
            total_reward += reward
            state = new_state
            if is_done:
                break
        
        return total_reward

    def value_iteration(self):
        num_states = self.env.observation_space.n
        num_actions = self.env.action_space.n
        self.value_table = np.zeros(num_states)
        
        for _ in range(1000):  # You can adjust the number of iterations
            new_value_table = np.zeros(num_states)
            for state in range(num_states):
                action_values = [self.calc_action_value(state, action) for action in range(num_actions)]
                new_value_table[state] = max(action_values)
            self.value_table = new_value_table

    def print_value_table(self):
        print("Value Table:")
        print(self.value_table.reshape((4, 4)))  # Assuming a 4x4 grid

    def extract_policy(self):
        policy = np.zeros(self.env.observation_space.n)
        for state in range(self.env.observation_space.n):
            action_values = [self.calc_action_value(state, action) for action in range(self.env.action_space.n)]
            policy[state] = np.argmax(action_values)
        return policy

    def print_policy(self, policy):
        print("Policy:")
        print(policy.reshape((4, 4)))  # Assuming a 4x4 grid

if __name__ == "__main__":
    test_env = Agent.create_env()
    agent = Agent()
    iter_no = 0
    best_reward = 0

    while True:
        iter_no += 1
        agent.play_n_random_steps(100)
        agent.value_iteration()
        reward = agent.play_episode(test_env)
        
        if reward > best_reward:
            print("Best reward updated %.3f -> %.3f" % (best_reward, reward))
            best_reward = reward
        
        if reward > 0.80:
            print("Solved in %d iterations!" % iter_no)
            agent.print_value_table()
            policy = agent.extract_policy()
            agent.print_policy(policy)
            break

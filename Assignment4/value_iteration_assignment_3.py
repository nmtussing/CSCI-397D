import gymnasium as gym
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
        self.rewards = collections.defaultdict(float)
        self.transits = collections.defaultdict(collections.Counter)
        self.values = np.zeros(self.env.observation_space.n)

    @staticmethod
    def create_env():
        return gym.make(ENV_NAME)

    def update_transits_rewards(self, state, action, new_state, reward):
        key = (state, action)
        self.rewards[key, new_state] = reward
        self.transits[key][new_state] += 1

    def play_n_random_steps(self, count):
        for _ in range(count):
            action = self.env.action_space.sample()
            new_state, reward, is_done, _ = self.env.step(action)
            self.update_transits_rewards(self.state, action, new_state, reward)
            self.state = self.env.reset() if is_done else new_state

    def print_value_table(self):
        print("Value Table:")
        print(self.values.reshape((4, 4)))

    def extract_policy(self):
        policy = np.zeros(self.env.observation_space.n, dtype=int)
        for state in range(self.env.observation_space.n):
            action_values = [self.calc_action_value(state, action) for action in range(self.env.action_space.n)]
            policy[state] = np.argmax(action_values)
        return policy

    def print_policy(self, policy):
        action_names = ["Left", "Down", "Right", "Up"]
        policy_grid = np.array([action_names[policy[state]] for state in range(self.env.observation_space.n)])
        print("Policy:")
        print(policy_grid.reshape((4, 4)))

    def calc_action_value(self, state, action):
        target_counts = self.transits[state, action]
        total_transitions = sum(target_counts.values())
        action_value = 0

        for new_state, count in target_counts.items():
            reward = self.rewards[state, action, new_state]
            action_value += (count / total_transitions) * (reward + GAMMA * self.values[new_state])

        return action_value

    def select_action(self, state):
        best_action, best_value = None, None
        for action in range(self.env.action_space.n):
            action_value = self.calc_action_value(state, action)
            if best_value is None or action_value > best_value:
                best_action, best_value = action, action_value
        return best_action

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
        for state in range(self.env.observation_space.n):
            state_values = [self.calc_action_value(state, action) for action in range(self.env.action_space.n)]
            self.values[state] = max(state_values)

if __name__ == "__main__":
    test_env = Agent.create_env()
    agent = Agent()
    iter_no = 0
    best_reward = 0

    while True:
        iter_no += 1
        agent.play_n_random_steps(100)
        agent.value_iteration()

        total_reward = 0
        for _ in range(TEST_EPISODES):
            total_reward += agent.play_episode(test_env)

        reward = total_reward / TEST_EPISODES

        if reward > best_reward:
            print("Best reward updated %.3f -> %.3f" % (best_reward, reward))
            best_reward = reward

        if reward > 0.80:
            print("Solved in %d iterations!" % iter_no)
            agent.print_value_table()
            policy = agent.extract_policy()
            agent.print_policy(policy)
            break

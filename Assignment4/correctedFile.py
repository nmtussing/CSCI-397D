import gym
import collections
import numpy as np

ENV_NAME = "FrozenLake-v1"
GAMMA = 0.9
TEST_EPISODES = 20
MAX_ITERATIONS = 1000  # Set a maximum for iterations to avoid infinite loops

class Agent:
    def __init__(self):
        self.env = gym.make(ENV_NAME, is_slippery=False, new_step_api=True)
        self.state = self.env.reset()
        self.stateNum = self.env.observation_space.n
        self.actionNum = self.env.action_space.n
        self.rewards = collections.defaultdict(lambda: collections.defaultdict(float))
        self.transits = collections.defaultdict(collections.Counter)
        self.values = [0.0 for _ in range(self.stateNum)]

    @staticmethod
    def create_env():
        return gym.make(ENV_NAME, is_slippery=False)

    def update_transits_rewards(self, state, action, new_state, reward):
        key = (state, action)
        self.rewards[key][new_state] += reward
        self.transits[key][new_state] += 1

    def play_n_random_steps(self, count):
        for _ in range(count):
            action = self.env.action_space.sample()
            new_state, reward, done, truncated, _ = self.env.step(action)
            self.update_transits_rewards(self.state, action, new_state, reward)
            self.state = new_state
            if done:
                self.state = self.env.reset()

    def print_value_table(self):
        for i in range(self.stateNum):
            print('{:.2f}'.format(self.values[i]), end=" ")
            if (i + 1) % int(np.sqrt(self.stateNum)) == 0:
                print("")

    def calc_action_value(self, state, action):
        target_counts = self.transits[(state, action)]
        total = sum(target_counts.values())
        action_value = 0.0
        for tgt_state, count in target_counts.items():
            reward = self.rewards[(state, action)][tgt_state]
            action_value += (count / total) * (reward + GAMMA * self.values[tgt_state])
        return action_value

    def select_action(self, state):
        best_action, best_value = None, float('-inf')
        for action in range(self.actionNum):
            action_value = self.calc_action_value(state, action)
            if action_value > best_value:
                best_value = action_value
                best_action = action
        return best_action

    def play_episode(self, env):
        total_reward = 0.0
        state = env.reset()
        while True:
            action = self.select_action(state)
            new_state, reward, done, _ = env.step(action)
            self.update_transits_rewards(state, action, new_state, reward)
            total_reward += reward
            if done:
                break
            state = new_state
        return total_reward

    def value_iteration(self):
        for state in range(self.stateNum):
            state_values = [self.calc_action_value(state, action) for action in range(self.actionNum)]
            self.values[state] = max(state_values)

if __name__ == "__main__":
    test_env = Agent.create_env()
    agent = Agent()

    iter_no = 0
    best_reward = 0.0
    for iter_no in range(MAX_ITERATIONS):
        agent.play_n_random_steps(100)
        agent.value_iteration()

        reward = sum(agent.play_episode(test_env) for _ in range(TEST_EPISODES)) / TEST_EPISODES
        
        if reward > best_reward:
            print(f"Best reward updated {best_reward:.3f} -> {reward:.3f}")
            best_reward = reward

        if reward > 0.80:
            print(f"Solved in {iter_no} iterations!")
            agent.print_value_table()
            break
    else:
        print("Not solved within the maximum number of iterations.")

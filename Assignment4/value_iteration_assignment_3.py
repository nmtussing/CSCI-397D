import gym
import collections
from tensorboardX import SummaryWriter

ENV_NAME = "FrozenLake-v1"
GAMMA = 0.9
TEST_EPISODES = 20
SEED = 42


class Agent:
    def __init__(self):
        pass

    @staticmethod
    def create_env():
        pass

    def update_transits_rewards(self, state, action, new_state, reward):
        pass

    def play_n_random_steps(self, count):
        pass

    def print_value_table(self):
        pass

    def extract_policy(self):
        pass

    def print_policy(self, policy):
        pass

    def calc_action_value(self, state, action):
        pass

    def select_action(self, state):
        pass

    def play_episode(self, env):
        pass

    def value_iteration(self):
        pass


if __name__ == "__main__":
    test_env = Agent.create_env()
    agent = Agent()

    iter_no = None
    best_reward = None
    while True:
        iter_no += 1
        agent.play_n_random_steps(100)
        agent.value_iteration()

        reward = None
        if reward > best_reward:
            print("Best reward updated %.3f -> %.3f" % (best_reward, reward))

        if reward > 0.80:
            print("Solved in %d iterations!" % iter_no)
            agent.print_value_table()
            policy = agent.extract_policy()
            agent.print_policy(policy)
            break

import torch
import random, numpy as np
from pathlib import Path
from neural import MarioNet
from collections import deque

class Mario:
    """
    Reinforcement learning agent named Mario that uses a variant of the Deep Q-Network (DQN) algorithm.

    Attributes:
        state_dim (tuple): The dimension of the state space.
        action_dim (int): The number of possible actions.
        memory (deque): A fixed-length deque to store experiences for replay.
        batch_size (int): The size of the batch to be used for learning.
        exploration_rate (float): Initial exploration rate for the ε-greedy policy.
        exploration_rate_decay (float): Decay rate for the exploration rate.
        exploration_rate_min (float): Minimum exploration rate.
        gamma (float): Discount factor for future rewards.
        curr_step (int): Counter for the current step.
        burnin (int): Number of steps to populate the memory before learning starts.
        learn_every (int): Number of steps between learning updates.
        sync_every (int): Number of steps between synchronizing the target and online networks.
        save_every (int): Number of steps between saving the current model.
        save_dir (Path): Directory for saving model checkpoints.
        use_cuda (bool): Flag to determine if CUDA is available for GPU acceleration.
        net (MarioNet): Neural network for approximating the Q-function.
        optimizer (torch.optim.Adam): Optimizer for training the network.
        loss_fn (torch.nn.SmoothL1Loss): Loss function used during training.
    """

    def __init__(self, state_dim, action_dim, save_dir, checkpoint=None):
        # Initialize the Mario agent with the given state and action dimensions, save directory, and optional checkpoint
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.memory = deque(maxlen=100000)  # Experience replay memory
        self.batch_size = 32

        # Exploration parameters for ε-greedy strategy
        self.exploration_rate = 1
        self.exploration_rate_decay = 0.99999975
        self.exploration_rate_min = 0.1
        self.gamma = 0.9  # Discount factor

        # Learning and synchronization parameters
        self.curr_step = 0
        self.burnin = 1e5  # Steps to fill the memory before learning
        self.learn_every = 3  # Frequency of learning updates
        self.sync_every = 1e4  # Frequency of syncing the target network

        self.save_every = 5e5  # Frequency of saving the model
        self.save_dir = save_dir

        # Initialize the neural network
        self.use_cuda = torch.cuda.is_available()
        self.net = MarioNet(self.state_dim, self.action_dim).float()
        if self.use_cuda:
            self.net = self.net.to(device='cuda')
        if checkpoint:
            self.load(checkpoint)

        # Set up the optimizer and loss function for training
        self.optimizer = torch.optim.Adam(self.net.parameters(), lr=0.00025)
        self.loss_fn = torch.nn.SmoothL1Loss()

    def act(self, state):
        """
        Select an action for a given state using the ε-greedy policy.

        Args:
            state (array): The current state of the environment.

        Returns:
            int: The index of the selected action.
        """
        # Select action using ε-greedy policy
        if np.random.rand() < self.exploration_rate:
            action_idx = np.random.randint(self.action_dim)  # Explore: choose a random action
        else:
            state = torch.FloatTensor(state).cuda() if self.use_cuda else torch.FloatTensor(state)
            state = state.unsqueeze(0)
            action_values = self.net(state, model='online')  # Exploit: choose the best action based on the online network
            action_idx = torch.argmax(action_values, axis=1).item()

        # Decay the exploration rate and increment the step counter
        self.exploration_rate *= self.exploration_rate_decay
        self.exploration_rate = max(self.exploration_rate_min, self.exploration_rate)
        self.curr_step += 1
        return action_idx

    def cache(self, state, next_state, action, reward, done):
        """
        Store an experience tuple in the replay memory.

        Args:
            state (array): The current state.
            next_state (array): The state after taking the action.
            action (int): The action taken.
            reward (float): The reward received.
            done (bool): Whether the episode has ended.
        """
        # Convert experience data to appropriate torch tensor types
        state = torch.FloatTensor(state).cuda() if self.use_cuda else torch.FloatTensor(state)

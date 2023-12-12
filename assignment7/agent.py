import torch
import random, numpy as np
from pathlib import Path

from neural import MarioNet
from collections import deque


class Mario:
    
    """
    Initializing the learning agent for the Mario game using Double DQN framework
    """
    def __init__(self, state_dim, action_dim, save_dir, checkpoint=None):
        # initializing agent with state, action dimensitons, save directory
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.memory = deque(maxlen=100000)
        self.batch_size = 32

        #Exploration parameters for epsilon greedy strategy 
        self.exploration_rate = 1
        self.exploration_rate_decay = 0.99999975
        self.exploration_rate_min = 0.1
        self.gamma = 0.9

        # learning and syncing parameters
        self.curr_step = 0
        self.burnin = 1e5  
        self.learn_every = 3   
        self.sync_every = 1e4   

        #saving frequency for the model 
        self.save_every = 5e5   
        self.save_dir = save_dir

        #initializing the neural net 
        self.use_cuda = torch.cuda.is_available()
        self.net = MarioNet(self.state_dim, self.action_dim).float()
        if self.use_cuda:
            self.net = self.net.to(device='cuda')
        if checkpoint:
            self.load(checkpoint)

        #setting up the optimizer and loss function
        self.optimizer = torch.optim.Adam(self.net.parameters(), lr=0.00025)
        self.loss_fn = torch.nn.SmoothL1Loss()


    """
    Action selection function for a given state using epsilon greedy policy 
    args: 
        state
    returns: 
        index of the action
    """
    def act(self, state):

        #selecting action using geedy policy
        if np.random.rand() < self.exploration_rate:
            action_idx = np.random.randint(self.action_dim)

        else:
            state = torch.FloatTensor(state).cuda() if self.use_cuda else torch.FloatTensor(state)
            state = state.unsqueeze(0)
            # The action is selected using the online network
            action_values = self.net(state, model='online')
            action_idx = torch.argmax(action_values, axis=1).item()

        #decaying exploration rate and incrementing step counter
        self.exploration_rate *= self.exploration_rate_decay
        self.exploration_rate = max(self.exploration_rate_min, self.exploration_rate)

        self.curr_step += 1
        return action_idx

        """
        Storing experiences in memory replay
        Args:   
            state, next state after taking the action, action taken, reward received, done (whether the episode is done or not (bool)
        """
        
    def cache(self, state, next_state, action, reward, done):

        state = torch.FloatTensor(state).cuda() if self.use_cuda else torch.FloatTensor(state)
        next_state = torch.FloatTensor(next_state).cuda() if self.use_cuda else torch.FloatTensor(next_state)
        action = torch.LongTensor([action]).cuda() if self.use_cuda else torch.LongTensor([action])
        reward = torch.DoubleTensor([reward]).cuda() if self.use_cuda else torch.DoubleTensor([reward])
        done = torch.BoolTensor([done]).cuda() if self.use_cuda else torch.BoolTensor([done])

        self.memory.append( (state, next_state, action, reward, done,) )

        """
        Function to sample experiences from replay memory
        
        """
    def recall(self):
        #batch sampling from memory 
        batch = random.sample(self.memory, self.batch_size)
        state, next_state, action, reward, done = map(torch.stack, zip(*batch))
        return state, next_state, action.squeeze(), reward.squeeze(), done.squeeze()

        """
        Function to estimate the current-Q value based on the current action
        """
    def td_estimate(self, state, action):
        # The 
        #estimating q-value for current action
        current_Q = self.net(state, model='online')[np.arange(0, self.batch_size), action] # Q_online(s,a)
        return current_Q

    # The target network is then used to calculate the estimated Q-value
        """Function to calculate TD target

        Args:
            reward, next state, done boolean 
        """
    @torch.no_grad()
    def td_target(self, reward, next_state, done):
        # next state q value using online network 
        next_state_Q = self.net(next_state, model='online')
        #epsilon greedy policy
        best_action = torch.argmax(next_state_Q, axis=1)
        #evaluation using the target network 
        next_Q = self.net(next_state, model='target')[np.arange(0, self.batch_size), best_action]
        return (reward + (1 - done.float()) * self.gamma * next_Q).float()

    """
        Updates the online network by minimizing the loss between TD estimates and targets.
        args:
            td estimate, td target
    """
    def update_Q_online(self, td_estimate, td_target) :
        #calculating the loss 
        loss = self.loss_fn(td_estimate, td_target)
        #optimizing function
        self.optimizer.zero_grad()
        #using backwards propogation
        loss.backward()
        self.optimizer.step()
        return loss.item()

        """Function to sync the target and online networks
        """
    def sync_Q_target(self):
        self.net.target.load_state_dict(self.net.online.state_dict())

        """Learning loop for the agent 
        """
    def learn(self):
        # checks the step counter for syncing the target and online networks
        if self.curr_step % self.sync_every == 0:
            self.sync_Q_target()
        # checking the save condition to save the model 
        if self.curr_step % self.save_every == 0:
            self.save()
        # checking to see if enough experiences have been accumulated
        if self.curr_step < self.burnin:
            return None, None
        #learning step tracker
        if self.curr_step % self.learn_every != 0:
            return None, None
        #sampling experiences 
        state, next_state, action, reward, done = self.recall()
        #Estimating the current q-val
        td_est = self.td_estimate(state, action)
        #evaluating the target
        td_tgt = self.td_target(reward, next_state, done)
        #updating the online network
        loss = self.update_Q_online(td_est, td_tgt)

        return (td_est.mean().item(), loss)

    """Function to save experiences
    """
    def save(self):
        save_path = self.save_dir / f"mario_net_{int(self.curr_step // self.save_every)}.chkpt"
        torch.save(
            dict(
                model=self.net.state_dict(),
                exploration_rate=self.exploration_rate
            ),
            save_path
        )
        print(f"MarioNet saved to {save_path} at step {self.curr_step}")


    def load(self, load_path):
        if not load_path.exists():
            raise ValueError(f"{load_path} does not exist")

        ckp = torch.load(load_path, map_location=('cuda' if self.use_cuda else 'cpu'))
        exploration_rate = ckp.get('exploration_rate')
        state_dict = ckp.get('model')

        print(f"Loading model at {load_path} with exploration rate {exploration_rate}")
        self.net.load_state_dict(state_dict)
        self.exploration_rate = exploration_rate

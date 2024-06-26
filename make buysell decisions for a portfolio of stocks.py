# -*- coding: utf-8 -*-
"""Untitled7.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1yp37R84o-6NOGTYIO3GAU_6ghe0dEwKR
"""

import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import yfinance as yf

def initialize_q_table(num_states, num_actions):
    return np.zeros((num_states, num_actions))

def select_action(q_table, state, epsilon):
    if random.uniform(0, 1) < epsilon:   #explore
        return random.randint(0, q_table.shape[1] - 1)
    else:
        return np.argmax(q_table[state, :])   #exploit

def update_q_values(q_table, state, action, reward, next_state, alpha, gamma):
    best_next_action = np.argmax(q_table[next_state, :])
    q_table[state, action] += alpha * (reward + gamma * q_table[next_state, best_next_action] - q_table[state, action])

def train_q_learning(data, epsilon=0.2, alpha=0.1, gamma=0.9, num_episodes=1000):
    num_states = len(data) - 1
    num_actions = 3

    q_table = initialize_q_table(num_states, num_actions)

    for episode in range(num_episodes):
        state = 0

        while state < num_states - 1:
            action = select_action(q_table, state, epsilon)

            # Simulate the trading environment and get the reward
            reward = calculate_reward(data['Close'].values, state, action)

            next_state = state + 1

            # Update Q-values based on the Bellman equation
            update_q_values(q_table, state, action, reward, next_state, alpha, gamma)

            state = next_state

    return q_table

def calculate_reward(prices, current_step, action):
    current_price = prices[current_step]
    next_price = prices[current_step + 1]

    if action == 0:
        return next_price - current_price
    elif action == 1:
        return 0
    elif action == 2:
        return current_price - next_price

data = pd.read_csv('/content/TATASTEEL1.NS.csv')

q_table = train_q_learning(data)

ticker="tata steel"

data=yf.download(ticker,period='6mo')

from matplotlib.pyplot import figure
figure(figsize=(20, 7), dpi=80)
plt.plot(data.Open)
plt.show()

figure(figsize=(15,7),dpi=80)
plt.plot(data.Volume)
plt.show()

figure(figsize=(25,7),dpi=80)
plt.plot(data.High)
plt.show()

figure(figsize=(25,7),dpi=80)
plt.plot(data.Low)
plt.show()

figure(figsize=(25,7),dpi=80)
plt.plot(data.Close)
plt.show()

current_state = 0
while current_state < len(data) - 1:
    if current_state < q_table.shape[0]:  # Check if current_state is within bounds
        action = np.argmax(q_table[current_state, :])
        print(f"Day {current_state + 1}: Action {action} (0: Buy, 1: Hold, 2: Sell)")
    current_state += 1
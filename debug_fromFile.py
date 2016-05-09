import numpy as np
import random
import time
from tqdm import tqdm
import sys, DLFCN
sys.setdlopenflags(DLFCN.RTLD_NOW | DLFCN.RTLD_GLOBAL)
import lua
lua.require('xlua')
Brain = lua.require("deepql_model/deepqlearn")
from game256 import *

#######  LUA & PYTHON for learning Game 2048 with Deep Reinforcement Learning #######

__author__ = 'Wonjun'


# params #
num_of_train = 50000
num_actions = 4
num_states = 16

Brain.init(num_states, num_actions)
Brain.load("inf_model.net")
Brain.gamma = 0.95
actions = ['H','P','K','M']

init_game()
global matrix
matrix = get()
prev_matrix = list(matrix)
total_game = 0.0
win_game = 0.0
output()
print matrix
print '---INIT---'
Brain.learning = False
for k in tqdm(range(100000)):
    reward = 0.0
    mc = bit_conversion(matrix)
    state_str = '{' + str(mc).strip('[]') + '}'
    state = lua.eval(state_str)
    #forward
    action_num = Brain.forward(state)
    #move
    #until reaching the possible movements
    #output()
    time.sleep(0.5)
    while True:
        output_action(action_num)
        move(actions[action_num-1])
        if matrix != prev_matrix:
            break
        else :
            Brain.backward(-1.0)
            #print "MOVING IMPOSSIBLE"
            action_num = Brain.forward(state)
    insert(matrix)
    prev_matrix = list(matrix)
    output()
    if max(matrix) == 128:
        print '128 MADE!!'
        reward = 1.0
        Brain.backward(reward)
        init_game()
        matrix = get()
        prev_matrix = list(matrix)
        win_game = win_game + 1
        total_game = total_game + 1
    if ( isOver(matrix) == False):
        # reward
        reward = 0
        Brain.backward(reward)
        #print  '----------------------------------'
    else:
        reward = -1.0
        Brain.backward(reward)
        matrix = get()
        print '---RE-INIT---'
        #print 'matrix = ', matrix
        prev_matrix = list(matrix)
        total_game = total_game + 1
        #print 'prev_matrix = ', prev_matrix
        output()

print (win_game / total_game)

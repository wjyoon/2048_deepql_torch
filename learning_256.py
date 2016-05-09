import numpy as np
import random
import time
import math
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
num_of_train = 100000
num_actions = 4
num_states = 192

Brain.init(num_states, num_actions)
Brain.load("inf_model_256.net")
#print "temp_window ", Brain.temporal_window
# Manipulating params of Nets #
Brain.start_learn_threshold = 2000
Brain.learning_steps_total = 100000
Brain.learning_steps_burnin = 2000
Brain.gamma = 0.95
actions = ['H','P','K','M']
#Brain.age = 1

total_game = 0.0
win_game = 0.0
#print prev_matrix
#output()
print '---INIT---'
#Brain.learning = False;
while True:
    f = open("win_rate.log","a")
    init_game()
    global matrix
    matrix = get()
    prev_matrix = list(matrix)
    total_game = 0.0
    win_game = 0.0
    output()
    print '------INIT-------'
    for k in tqdm(range(20000)):
        #time.sleep(1.5)
        if k!= 0 and k%500 == 0:
	    print "win_rate = ", win_game / total_game
	    #print "total_game = ", total_game
        reward = 0.0
        matrix_converted = bit_conversion(matrix)
        state_str = '{' + str(matrix_converted).strip('[]') + '}'
        state = lua.eval(state_str)
        #forward
        action_num = Brain.forward(state)
        while True:
	    move(actions[action_num-1])
	    if matrix != prev_matrix:
	        break
	    else :
                reward = -10.0
                Brain.backward(reward)
	        print "MOVING IMPOSSIBLE"
	        action_num = Brain.forward(state)
        insert(matrix)
        matrix_converted = bit_conversion(matrix)
        prev_matrix = list(matrix)
        output()
        if max(matrix) == 256:
    	    print "total_reware = ", reward
	    reward = 800.0
	    Brain.backward(reward)
	    init_game()
	    matrix = get()
	    prev_matrix = list(matrix)
	    win_game = win_game + 1
	    total_game = total_game + 1
	    continue
        if ( isOver(matrix) == False):
	    # reward
	    reward = 0
	    #reward = reward + monotonicity() #TO BE FIXED
	    #reward = reward + smoothness()
	    #reward = reward + freetiles()
	    #reward = reward + math.log(float(max(matrix))) / math.log(2) /10
	    #reward = reward
	    print "total_reward = ", reward
            #backward
	    Brain.backward(reward)
	    #print  '----------------------------------'
        else:
	    #print "FAILED"
	    reward = -500.0
	    Brain.backward(reward)
            init_game()
    	    matrix = get()
	    #print 'matrix = ', matrix
   	    prev_matrix = list(matrix)
	    total_game = total_game + 1
	    #output()
    f.write(str(win_game / total_game))
    Brain.save("inf_model_256", Brain.net)
    f.close()

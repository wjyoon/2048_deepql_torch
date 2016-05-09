#!/usr/bin/env python
# encoding: utf-8
"""
The minigame 2048 in python
"""
import math
import random
def init():
    """
    initialize a 2048 matrix. return a matrix list
    """
    global score, matrix, total_score
    score = 0
    total_score = 0
    matrix = [ 0 for i in range(16) ]
    random_lst = random.sample( range(16), 2 ) # generate 2 different number
    matrix[random_lst[0]] = matrix[random_lst[1]] = 2
    return matrix

def virtual_move(matrix,direction):
    """
    moving the new. return a new list
    """
    new = list(matrix)
    global score
    global prev_score 
    prev_score = score
    mergedList = [] #initial the merged index
    if direction == 'H':
        for i in range(16):
            j = i
            while j - 4 >= 0:
                if new[j-4] == 0:
                    new[j-4] = new[j]
                    new[j] = 0
                elif new[j-4] == new[j] and j - 4 not in mergedList and j not in mergedList:
                    new[j-4] *=2
                    score = score + new[j-4]
                    new[j] = 0
                    mergedList.append(j-4)
                    mergedList.append(j)  #prevent the number to be merged twice
                j -= 4
    elif direction == 'P':
        for i in range(15,-1,-1):
            j = i
            while j + 4 < 16:
                if new[j+4] == 0:
                    new[j+4] = new[j]
                    new[j] = 0
                elif new[j+4] == new[j] and j + 4 not in mergedList and j not in mergedList:
                    new[j+4] *=2
                    score = score + new[j+4]
                    new[j] = 0
                    mergedList.append(j)
                    mergedList.append(j+4)
                j += 4
    elif direction == 'K':
        for i in range(16):
            j = i
            while j % 4 != 0:
                if new[j-1] == 0:
                    new[j-1] = new[j]
                    new[j] = 0
                elif new[j-1] == new[j] and j - 1 not in mergedList and j not in mergedList:
                    new[j-1] *=2
                    score = score + new[j-1]
                    new[j] = 0
                    mergedList.append(j-1)
                    mergedList.append(j)
                j -= 1
    else:
        for i in range(15,-1,-1):
            j = i
            while j % 4 != 3:
                if new[j+1] == 0:
                    new[j+1] = new[j]
                    new[j] = 0
                elif new[j+1] == new[j] and j + 1 not in mergedList and j not in mergedList:
                    new[j+1] *=2
                    score = score + new[j+1]
                    new[j] = 0
                    mergedList.append(j)
                    mergedList.append(j+1)
                j += 1
    return new


def heuristic_move(matrix):
    # for x in possible choices
    # calculate smoothness, monotonicity, emptycells
    # choose largest one as an action
    prev_matrix = list(matrix)
    psbl_actions = determine_possibleMove(matrix)
    sum = [0.0 for x in range(len(psbl_actions))]
    for i in range(len(psbl_actions)):
        new_matrix = virtual_move(prev_matrix,psbl_actions[i])
        sum[i] = sum[i] + smoothness(new_matrix)
        sum[i] = sum[i] + monotonicity(new_matrix)
        sum[i] = sum[i] + freetiles(new_matrix)
    max_idx = max((v,i) for i, v in enumerate(sum) )[1]
    return psbl_actions[max_idx]

def determine_possibleMove(matrix):
    psbl_actions = ['H','P','K','M']
    prev_matrix = list(matrix)
    cnt = list()
    for i in range(4):
        new_matrix = virtual_move(prev_matrix,psbl_actions[i])
        if(matrix != new_matrix):
            cnt.append(i)
    #print "cnt = ", cnt
    #for i in range(len(cnt)):
        #print "Possible move = "
        #output_action(cnt[i]) 
    result_actions = list()
    for i in range(len(cnt)):
        result_actions.append(psbl_actions[cnt[i]])
    #print "result_actions", result_actions
    return result_actions


def move(direction):
    global matrix
    """
    moving the matrix. return a matrix list
    """
    global score,prev_score

    prev_score = score
    mergedList = [] #initial the merged index
    if direction == 'H':
        for i in range(16):
            j = i
            while j - 4 >= 0:
                if matrix[j-4] == 0:
                    matrix[j-4] = matrix[j]
                    matrix[j] = 0
                elif matrix[j-4] == matrix[j] and j - 4 not in mergedList and j not in mergedList:
                    matrix[j-4] *=2
                    score = score + matrix[j-4]
                    matrix[j] = 0
                    mergedList.append(j-4)
                    mergedList.append(j)  #prevent the number to be merged twice
                j -= 4
    elif direction == 'P':
        for i in range(15,-1,-1):
            j = i
            while j + 4 < 16:
                if matrix[j+4] == 0:
                    matrix[j+4] = matrix[j]
                    matrix[j] = 0
                elif matrix[j+4] == matrix[j] and j + 4 not in mergedList and j not in mergedList:
                    matrix[j+4] *=2
                    score = score + matrix[j+4]
                    matrix[j] = 0
                    mergedList.append(j)
                    mergedList.append(j+4)
                j += 4
    elif direction == 'K':
        for i in range(16):
            j = i
            while j % 4 != 0:
                if matrix[j-1] == 0:
                    matrix[j-1] = matrix[j]
                    matrix[j] = 0
                elif matrix[j-1] == matrix[j] and j - 1 not in mergedList and j not in mergedList:
                    matrix[j-1] *=2
                    score = score + matrix[j-1]
                    matrix[j] = 0
                    mergedList.append(j-1)
                    mergedList.append(j)
                j -= 1
    else:
        for i in range(15,-1,-1):
            j = i
            while j % 4 != 3:
                if matrix[j+1] == 0:
                    matrix[j+1] = matrix[j]
                    matrix[j] = 0
                elif matrix[j+1] == matrix[j] and j + 1 not in mergedList and j not in mergedList:
                    matrix[j+1] *=2
                    score = score + matrix[j+1]
                    matrix[j] = 0
                    mergedList.append(j)
                    mergedList.append(j+1)
                j += 1
    #return matrix

#def reach256(prev_matrix):
#    global matrix
#    for i in range(16):
#        if matrix[i] == 256:
#            return 1.0
#        else:
#            return 0.0

def smoothness(matrix):
    smoothness = 0.0
    val = 0.0
    for i in range(16):
        if matrix[i] != 0:
            val = math.log(matrix[i]) / math.log(2)
            #print "val = ", val
            right = findFarthestRight(matrix,i)
            down = findFarthestDown(matrix,i)
            if matrix[right] != 0:
              target_right = math.log(matrix[right]) / math.log(2)
              #print "target_right = ", target_right
              smoothness = smoothness + abs(val - target_right)
            if matrix[down] != 0:  
              target_down = math.log(matrix[down]) / math.log(2)
              #print "target_right = ", target_down
              smoothness = smoothness + abs(val - target_down)
    #print "smoothness = ", smoothness / 10
    return smoothness /10
    #result = 0.0
    #if smoothness <= 30:
    #    result = 1.0
    #elif smoothness <= 40 and smoothness > 30:
    #    result = 0.8
    #elif smoothness <= 50 and smoothness > 40:
    #    result = 0.4
    #elif smoothness <= 60 and smoothness > 50:
    #    result = 0.2
    #elif smoothness <= 70 and smoothness > 60:
    #    result = 0.0
    #elif smoothness <= 80 and smoothness > 70:
    #    result = -0.2
    #else:
    #    result = -0.4
    #result = result / 25
    #print "smoothness ", result
    #return result

def findFarthestRight(matrix, index):
    result = 0
    if index/4 == 0:
        for i in range(index+1, 4):
            if matrix[i] != 0:
                result = i
    elif index/4 == 1:
        for i in range(index+1, 8):
            if matrix[i] != 0:
                result = i
    elif index/4 == 2:
        for i in range(index+1, 12):
            if matrix[i] != 0:
                result = i
    elif index/4 == 3:
        for i in range(index+1, 16):
            if matrix[i] != 0:
                result = i
    return result

def findFarthestDown(matrix, index):
    result = 0
    if index%4 == 0:
        for i in range(index+4, 13, 4):
            if matrix[i] != 0:
                result = i
    elif index%4 == 1:
        for i in range(index+4, 14, 4):
            if matrix[i] != 0:
                result = i
    elif index%4 == 2:
        for i in range(index+4, 15, 4):
            if matrix[i] != 0:
                result = i
    elif index%4 == 3:
        for i in range(index+4, 16, 4):
            if matrix[i] != 0:
                result =  i
    return result
def monotonicity(matrix):
  totals = [0,0,0,0]

  for x in range(4):
    current = 0
    currVal = 0
    nextVal = 0
    next = current +1
    while next < 4 :
      while (next < 4) and (matrix[x + 4*next] != 0):
        next = next + 1
      if next >= 4:
        next = next - 1
      if matrix[x + 4*current] != 0:
        currVal = math.log(matrix[x + 4*current]) / math.log(2)
      else:
        currVal = 0
      if matrix[x + 4*next] != 0:
        nextVal = math.log(matrix[x + 4*next]) / math.log(2)
      else:
        nextVal = 0
      if currVal > nextVal:
        totals[0] = totals[0] + nextVal - currVal
      elif nextVal > currVal:
        totals[1] = totals[1] + currVal - nextVal
      current = next
      next = next +1

  for y in range(4):
    current = 0
    currVal = 0
    nextVal = 0
    next = current +1
    while next < 4 :
      while (next < 4) and (matrix[4*y + next] != 0):
        next = next + 1
      if next >= 4:
        next = next - 1
      if matrix[4*y + current] != 0:
        currVal = math.log(matrix[4*y + current]) / math.log(2)
      else:
        currVal = 0
      if matrix[4*y + next] != 0:
        nextVal = math.log(matrix[4*y + next]) / math.log(2)
      else:
        nextVal = 0
      if currVal > nextVal:
        totals[2] = totals[0] + nextVal - currVal
      elif nextVal > currVal:
        totals[3] = totals[1] + currVal - nextVal
      current = next
      next = next +1
  mono = max(totals[0], totals[1]) + max(totals[2], totals[3])
  #print "mono = ", mono
  return mono
  #result = 0.0
  #if mono <= -10:
  #    result = 0.0
  #elif mono <= -6 and mono > -10:
  #    result = 0.1
  #elif mono <= -4 and mono > -6:
  #    result = 0.3
  #elif mono <= -2 and mono > -4:
  #    result = 0.7
  #elif mono <= -1 and mono > -2:
  #    result = 0.9
  #else:
  #    result = 1
  #result = result / 2
  #print "monotonicity = ", result
  #return result


def adjacent_diff():
    global matrix
    sum = 0.0
    for i in range(16):
        if i == 0:
            sum = sum + abs(matrix[0] - matrix[1])
            sum = sum + abs(matrix[0] - matrix[4])
        elif i == 1:
            sum = sum + abs(matrix[1] - matrix[0])
            sum = sum + abs(matrix[1] - matrix[2])
            sum = sum + abs(matrix[1] - matrix[5])
        elif i == 2:
            sum = sum + abs(matrix[2] - matrix[1])
            sum = sum + abs(matrix[2] - matrix[3])
            sum = sum + abs(matrix[2] - matrix[6])
        elif i == 3:
            sum = sum + abs(matrix[3] - matrix[2])
            sum = sum + abs(matrix[3] - matrix[7])
        elif i == 4:
            sum = sum + abs(matrix[4] - matrix[0])
            sum = sum + abs(matrix[4] - matrix[5])
            sum = sum + abs(matrix[4] - matrix[8])
        elif i == 5:
            sum = sum + abs(matrix[5] - matrix[1])
            sum = sum + abs(matrix[5] - matrix[4])
            sum = sum + abs(matrix[5] - matrix[6])
            sum = sum + abs(matrix[5] - matrix[9])
        elif i == 6:
            sum = sum + abs(matrix[6] - matrix[2])
            sum = sum + abs(matrix[6] - matrix[5])
            sum = sum + abs(matrix[6] - matrix[7])
            sum = sum + abs(matrix[6] - matrix[10])
        elif i == 7:
            sum = sum + abs(matrix[7] - matrix[3])
            sum = sum + abs(matrix[7] - matrix[6])
            sum = sum + abs(matrix[7] - matrix[11])
        elif i == 8:
            sum = sum + abs(matrix[8] - matrix[4])
            sum = sum + abs(matrix[8] - matrix[9])
            sum = sum + abs(matrix[8] - matrix[12])
        elif i == 9:
            sum = sum + abs(matrix[9] - matrix[5])
            sum = sum + abs(matrix[9] - matrix[8])
            sum = sum + abs(matrix[9] - matrix[10])
            sum = sum + abs(matrix[9] - matrix[13])
        elif i == 10:
            sum = sum + abs(matrix[10] - matrix[6])
            sum = sum + abs(matrix[10] - matrix[9])
            sum = sum + abs(matrix[10] - matrix[11])
            sum = sum + abs(matrix[10] - matrix[14])
        elif i == 11:
            sum = sum + abs(matrix[11] - matrix[7])
            sum = sum + abs(matrix[11] - matrix[10])
            sum = sum + abs(matrix[11] - matrix[15])
        elif i == 12:
            sum = sum + abs(matrix[12] - matrix[8])
            sum = sum + abs(matrix[12] - matrix[13])
        elif i == 13:
            sum = sum + abs(matrix[13] - matrix[9])
            sum = sum + abs(matrix[13] - matrix[12])
            sum = sum + abs(matrix[13] - matrix[14])
        elif i == 14:
            sum = sum + abs(matrix[14] - matrix[10])
            sum = sum + abs(matrix[14] - matrix[13])
            sum = sum + abs(matrix[14] - matrix[15])
        elif i == 15:
            sum = sum + abs(matrix[15] - matrix[11])
            sum = sum + abs(matrix[15] - matrix[14])
    #print "diffs in adjacent ", (sum / 1000)
    return sum /1000
'''
def smoothness():
    global prev_score, score
    val = 0.0
    diff = score - prev_score

    if diff > 0 and diff < 20:
        val = 0.0
    elif diff >= 20 and diff < 40:
        val = 0.2
    elif diff >= 40 and diff < 80:
        val = 0.4
    elif diff >= 80 and diff < 160:
        val = 0.6
    elif diff >= 160 and diff < 320:
        val = 0.8
    elif diff >= 320:
        val = 1.0
    else:
        val = 0.0
    #print "smoothnes val ", val, " diffs = ", diff
    return val
'''
def freetiles(matrix):
    val = 0.0
    cnt = 0
    for i in range(16):
        if matrix[i] == 0:
            cnt = cnt + 1
    val = math.log(float(cnt)) * 8.0
    #print "freetiles = ", val
    return val
    #if cnt == 3:
    #    val = -0.2
    #elif cnt == 2:
    #    val = -0.4
    #elif cnt == 1:
    #    val = -0.8
    #elif cnt == 0:
    #    val = -1.0
    #elif cnt == 4:
    #    val = 0.2
    #elif cnt == 5:
    #    val = 0.3
    #elif cnt == 6:
    #    val = 0.4
    #else:
    #    val = 0.5

    #print "freetiles val ", val
    #return val




def get():
    global matrix
    return matrix

def insert(matrix):
    """insert one 2 or 4 into the matrix. return the matrix list
    """
    getZeroIndex = []
    for i in range(16):
        if matrix[i] == 0:
            getZeroIndex.append(i)
    ##print "ZERO INDEX = ", getZeroIndex
    randomZeroIndex = random.choice(getZeroIndex)
    r = random.random()
    if (r < 0.9):
        matrix[randomZeroIndex] = 2
    else:
        matrix[randomZeroIndex] = 4
    #return matrix

def output():
    global matrix
    """
    #print the matrix. return the matrix list
    """
    max_num_width = len(str(max(matrix)))
    demarcation = ( '+' + '-'*(max_num_width+2) ) * 4 + '+' #generate demarcation line like '+---+---+---+'
    print demarcation
    for i in range(len(matrix)):
        if matrix[i] == 0:
            printchar = ' '
        else:
            printchar = str(matrix[i])
        print '|', 
        print '{0:>{1}}'.format(printchar,max_num_width),
        if (i + 1) % 4 == 0:
            print '|'
            print demarcation
    print

def output_action(action_num):
    if action_num == 3:
		    print 'RIGHT'
    elif action_num == 2:
		    print 'LEFT'
    elif action_num == 1:
        print 'DOWN'
    elif action_num == 0:
        print 'UP'

def isOver(matrix):
    """is game over? return bool
    """
    if 0 in matrix:
        return False
    else:
        for i in range(16):
            if i % 4 != 3:
                if matrix[i] == matrix[i+1]:
                    return False
            if i < 12:
                if matrix[i] == matrix [i+4]:
                    return False
    #print "GAME OVER"
    #GAME RE-INITIATE
    init_game()
    return True
def init_game():
    global matrix
    matrix = init()
    matrix_stack = []
    matrix_stack.append(list(matrix))
    step = len(matrix_stack) - 1
'''
def play():
    matrix = init()
    matrix_stack = [] # just used by back function
    matrix_stack.append(list(matrix))
    step = len(matrix_stack) - 1

    while True:
        output(matrix)
        if isOver(matrix) == False:
            if max(matrix) == 2048:
                input = raw_input('The max number is 2048, win the goal! q for quit, others for continue. ')
                if input == 'q':
                    exit()
            while True:
                #print "Step {0:2d} Use the arrow keys to move to corresponding direction, q for quit, b for back: ".format(step)
                input = ord(msvcrt.getch())
                if input == 224:         #Special keys 
                    input = msvcrt.getch()
                    if input in [ 'H', 'P', 'K', 'M' ]:
                        matrix = move(matrix,input)
                        if matrix == matrix_stack[-1]:
                            #print 'Not chaged. Try another direction.'
                        else:
                            insert(matrix)
            	        matrix_stack.append(list(matrix))
                        break
                elif input == 98:              #'b'=98
                    if len(matrix_stack) == 1:
                        #print 'Cannot back anymore...'
                        continue
                    matrix_stack.pop()
                    matrix = list(matrix_stack[-1])
                    break
                elif input == 113:          #'q'=113
                    #print 'Byebye!'
                    exit()
                else:
                    #print 'Input error! Try again.'
        else:
            #print 'Cannot move anyway. Game Over...'
            exit()
        step = len(matrix_stack) - 1
'''
if __name__ == '__main__':
    play()

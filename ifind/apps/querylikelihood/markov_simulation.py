__author__ = 'leif'
import sys
import argparse
import math
import random


def main():
    pm = [[0.0 for x in range(4)] for x in range(4)]

    pm[0][1]=1.0
    pm[1][0]=0.03
    pm[1][1]=0.87
    pm[1][2]=0.09
    pm[1][3]=0.01
    pm[2][0]=0.02
    pm[2][1]=0.74
    pm[2][3]=0.24
    pm[3][0]=0.15
    pm[3][1]=0.85


    t = [4.9, 2.3, 15.3, 1.7]



    def get_next_state(matrix, current_state, dice_roll):
        row = matrix[current_state]
        prob = row[0]

        if dice_roll <= prob:
            return 0

        prob = prob + row[1]

        if dice_roll <= prob:
            return 1

        prob = prob + row[2]


        if dice_roll <= prob:
            return 2
        else:
            return 3


    counts = [0, 0, 0, 0]
    for i in range(10000):
        s = get_next_state(pm,1,random.random())
        counts[s] +=1

    #print counts




    def run_sim(matrix, times):
        states = ['Query', 'Result','Detail','Basket']
        current_state = 0
        total_time = times[current_state]

        time_to_query = 0.0
        time_to_basket = 0.0
        results = 0
        details = 0
        cond = True
        seq = []
        while cond:
            seq.append(states[current_state])
            dice_roll = random.random()
            next_state = get_next_state(pm,current_state, dice_roll)



            if next_state ==1:
                if time_to_basket == 0.0:
                    results +=1

            if next_state ==2:
                if time_to_basket == 0.0:
                    details +=1


            total_time = total_time + times[next_state]

            if next_state == 0:
                if time_to_query == 0.0:
                    time_to_query = total_time

            if next_state == 3:
                if time_to_basket == 0.0:
                    time_to_basket = total_time

            cond = (time_to_query==0.0) or (time_to_basket==0.0)

            current_state = next_state

        seq.append(states[current_state])
        return (time_to_query, time_to_basket, seq, results, details)


    for i in range(10000):
        (tq, tb, seq, r, d) = run_sim(pm,t)
        print tq, tb, r, d



def usage(script_name):
    """
    Prints the usage message to the output stream.
    """
    print "Usage: {0}".format(script_name)

if __name__ == '__main__':
    main()
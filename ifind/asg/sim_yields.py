__author__ = 'leif'

from ifind.asg.asg_generator import RandomYieldGenerator, TestHighYieldGenerator, ConstantLinearYieldGenerator, TestYieldGenerator, CueGenerator, GainBasedCueGenerator
from ifind.asg.asg_generator import TestLowYieldGenerator, RandGainBasedCueGenerator

import numpy as np
from scipy.optimize import curve_fit
import math

ryg = RandomYieldGenerator()
tyg = TestYieldGenerator()
cyg = ConstantLinearYieldGenerator()
hyg = TestHighYieldGenerator()
lyg = TestLowYieldGenerator()


random_game = {'yield_generator': ryg,  'query_cost': 3.0, 'assess_cost': 1.0 }
high_game = {'yield_generator': hyg,  'query_cost': 2.0, 'assess_cost': 1.0 }
test_game = {'yield_generator': tyg,  'query_cost': 2.0, 'assess_cost': 1.0 }
low_cost_game = {'yield_generator': hyg, 'query_cost': 1.0, 'assess_cost': 2.0 }
cue_based_game = {'yield_generator': tyg, 'query_cost': 2.0, 'assess_cost': 1.0 }
low_game = {'yield_generator': lyg,  'query_cost': 2.0, 'assess_cost': 1.0 }




def sim_y(yg,n=200):
    m = 10
    y = [0.0] * m

    for i in range(0,n):
        ay = yg.get_yields()
        for j in range(0,m):
            y[j] += ay[j]
    cy = cum_sum(y)

    for j in range(0,m):
        cy[j] = cy[j]/float(n)


    return cy

def cum_sum(v):
    cv = [0.0] * len(v)
    cv[0] = v[0]
    for j in range(1,len(v)):
        cv[j] = cv[j-1] + v[j]
    return cv

def gain_time(cy, cq, ca):

    m = len(cy)
    gt = [0.0]*m

    for j in range(0,m):
        t = cq + j*ca
        gt[j] = cy[j] / t

    return gt



def test(y, cq, ca):
    ty = cum_sum(y)
    gt = gain_time(ty,cq,ca)
    return gt

def steps(y,avg_gt):
    m = len(y)
    i = 0
    while i<m:
        if y[i] > avg_gt:
            i = i + 1
        else:
            break
    return i


def get_yields(yg):
    y = yg.get_yields()
    return y



def run_sim(yg,n):
    cq = 2.0
    ca = 1.0

    cy = sim_y(yg,n)
    gt = gain_time(cy, cq,ca)
    print gt
    avg_gt = max(gt)
    print avg_gt

    for i in range(0,3):
        y1 = get_yields(yg)
        gt = gain_time(cum_sum(y1),cq,ca)
        print gt
        print y1
        s = steps(y1,avg_gt)
        print s



def fit_gain_function(y,cq,ca):


    y1 = list(y)
    n = len(y1)
    y1[:0] = [0.00001]
    x1 = (range(1,n+1)*ca)
    x1[:0]= [0.00001]

    x = np.array(x1)
    y = np.array(y1)

    def fit_func(x, a, b):
        return a*(x**b)

    params = curve_fit(fit_func, x, y)

    return params[0]

def find_stop_point(y,cq,ca,m):

    [k1,b1] = fit_gain_function(y,cq,ca)

    xn = (m / (k1*b1))**(1/(b1-1))
    return xn


yg = cyg

y = sim_y(yg)

print y

[k,b] = fit_gain_function(y,2,1)
print k,b

xs = 2*b/(1-b)
ys = k*(xs**b)
print xs,ys

m = ys/(xs--2)
print m


#[k1,b1] = fit_gain_function(y,2,1)
#print k1,b1
#print y

#xn = (m / (k1*b1))**(1/(b1-1))
#print "xn1 ", xn

y = sim_y(yg,n=1)
print y
xn =  find_stop_point(y,2,1,m)
print "xn1 ", math.ceil(xn)

y = sim_y(yg,n=1)
print y
xn =  find_stop_point(y,2,1,m)
print "xn2 ", math.ceil(xn)

y = sim_y(cyg,n=1)
print y
xn =  find_stop_point(y,2,1,m)
print "xn3 ", math.ceil(xn)

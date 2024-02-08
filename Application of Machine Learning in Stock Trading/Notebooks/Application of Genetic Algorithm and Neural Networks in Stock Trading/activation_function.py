import math    
import numpy as np

# activation function and its derivative
def tanh(x):
    return np.tanh(x)

def tanh_prime(x):
    return 1-np.tanh(x)**2

def sigmoid(x):
     return 1 / (1 + math.e ** -x) 

def sigmoid_derivative(a):
    return a * (1 - a)
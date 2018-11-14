import math
import random
import numpy as np

class RandomGenerator():   

    @staticmethod
    def ranf(lowLimit = 0.0, highLimit = 1.0):
       return random.uniform(lowLimit, highLimit)

    @staticmethod
    def granf(m = 0.0, v = 1.0):   
        return random.normalvariate(m, v) 

    @staticmethod
    def iranx(limit):        
        return random.randint(1, limit)
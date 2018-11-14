import math
import random
import numpy as np

class RandomGenerator():   

    @staticmethod
    def ranf(lowLimit = 0.0, highLimit = 1.0):
       return random.uniform(lowLimit, highLimit)

    @staticmethod
    def granf():   
        return random.normalvariate(0, 1.0) 

    @staticmethod
    def iranx(limit):        
        return random.randint(1, limit)
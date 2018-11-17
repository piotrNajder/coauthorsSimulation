import random

class RandomGenerator():   

    @staticmethod
    def randU(lowLimit = 0.0, highLimit = 1.0):
       return random.uniform(lowLimit, highLimit)

    @staticmethod
    def randN(m = 0.0, v = 1.0):   
        return random.normalvariate(m, v) 

    @staticmethod
    def randI(limit):        
        return random.randint(0, limit - 1)
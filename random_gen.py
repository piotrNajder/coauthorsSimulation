import random

class RandomGenerator():

    @staticmethod
    def ranf(lowLimit = 0.0, highLimit = 1.0):
        return random.uniform(lowLimit, highLimit)


    @staticmethod
    def granf(lowLimit = -2.0, highLimit = 2.0):
        return random.uniform(lowLimit, highLimit)

    @staticmethod
    def iranx(limit):
        return random.randint(1, limit)
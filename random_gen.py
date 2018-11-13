import math
import random

class RandomGenerator():

    @staticmethod
    def ranf(lowLimit = 0.0, highLimit = 1.0):
        return random.uniform(lowLimit, highLimit)


    @staticmethod
    def granf(lowLimit = -2.0, highLimit = 2.0):
        twopi = 6.28318530717958647        
        xx = RandomGenerator.ranf()

        xx1 = RandomGenerator.ranf()
        while xx1 > 0.9999:
            xx1 = RandomGenerator.ranf()
        
        return math.cos(twopi * xx) * math.sqrt( -2.0 * math.log(1.0 - xx1))

    @staticmethod
    def iranx(limit):        
        i = 1 + int(float(limit) * RandomGenerator.ranf())
        if (i > limit): i = limit
        elif (i < 1): i = 1
        return int(i)
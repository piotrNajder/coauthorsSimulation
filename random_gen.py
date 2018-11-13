import math
import random
import numpy as np

class RandomGenerator():

    _idum = 0
    _inext = 0
    _inextp = 0
    _iff = 0
    _ma = np.zeros(55)

    @staticmethod
    def _FMODL(i,j):
        if i < j:
            return i
        else:
            return RandomGenerator._FMODL(i - j, j)
    

    @staticmethod
    def ranf(lowLimit = 0.0, highLimit = 1.0):
        mbig = 1000000000
        mseed = 161803398 
        mz = 0
        fac = 100.0 / float(mbig)
        mj = 0
        mk = 0
        i = 0
        ii = 0
        k = 0
        iii = 0
        kk = 0

        if RandomGenerator._idum < 0 or RandomGenerator._iff == 0:
            RandomGenerator._iff = 1
            if RandomGenerator._idum >= 0:
                iii = RandomGenerator._idum
            else:
                iii = -RandomGenerator._idum

            mj = mseed - iii
            mj = RandomGenerator._FMODL(mj, mbig)
            RandomGenerator._ma[54] = mj
            mk = 1
            for i in range(1, 55):                
                ii = RandomGenerator._FMODL(21 * i, 55) - 1
                RandomGenerator._ma[ii] = mk
                mk = mj - mk
                if (mk < mz):
                    mk = mk + mbig
                mj = RandomGenerator._ma[ii]
                
            for k in range(1, 5):
                for i in range(1, 56):
                    kk = int( RandomGenerator._FMODL(i + 30,55) )
                    RandomGenerator._ma[i-1] = RandomGenerator._ma[i-1] - \
                                               RandomGenerator._ma[kk]
                    if(RandomGenerator._ma[i-1] < mz):
                        RandomGenerator._ma[i-1] = RandomGenerator._ma[i-1] + mbig
                
        RandomGenerator._inext = -1
        RandomGenerator._inextp = 30
        RandomGenerator._idum = 1

        RandomGenerator._inext += 1
        if(RandomGenerator._inext == 55):
            RandomGenerator._inext = 0

        RandomGenerator._inextp += 1
        if(RandomGenerator._inextp == 55):
            RandomGenerator._inextp = 0

        mj = RandomGenerator._ma[RandomGenerator._inext] - \
                                RandomGenerator._ma[RandomGenerator._inextp]

        if(mj < mz):
            mj = mj + mbig
        RandomGenerator._ma[RandomGenerator._inext] = mj
        return float( (mj / 100.0) * fac )

    @staticmethod
    def granf():        
        xx = RandomGenerator.ranf()
        xx1 = RandomGenerator.ranf()
        while xx1 > 0.9999:
            xx1 = RandomGenerator.ranf()
        
        return float(math.cos(2 * math.pi * xx) * \
                     math.sqrt( -2.0 * math.log(1.0 - xx1) ))

    @staticmethod
    def iranx(limit):        
        i = 1 + int(float(limit) * RandomGenerator.ranf())
        if (i > limit): i = limit
        elif (i < 1): i = 1
        return int(i)
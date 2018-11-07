import random

class RandomGenerator():

    @staticmethod
    def ranf():
        return random.uniform(0.0, 1.0)

    @staticmethod
    def granf():
        return random.uniform(-2.0, 2.0)

    @staticmethod
    def iranx(limit):
        return random.randint(1, limit)
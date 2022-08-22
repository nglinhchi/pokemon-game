"""
Random number generator class. Uses LCG method with some reasonable initialisation.
"""
__author__ = "Jackson Goerner"

import time

class RandomGen():
    """
    Class used to generate (seeded) random numbers for interesting outcomes and repeatable tests.
    
    Uses LCG method. All methods are O(1) best/worst case time complexity.
    
    Usage:
    ```
    RandomGen.set_seed(123)
    RandomGen.random()           # Random number from 0 to 2^32-1
    RandomGen.randint(1, 10)     # Random number from 1 to 10
    RandomGen.random_chance(0.33) # True 33% of the time, False 67% of the time.
    ```
    """
    
    MOD = pow(2, 48)
    A = 25214903917
    C = 11
    
    seed = time.time_ns()
    
    @classmethod
    def set_seed(cls, seed=None):
        """Seed all future calls to `random`."""
        seed = time.time_ns() if seed is None else seed
        cls.seed = seed
    
    @classmethod
    def random(cls):
        """Returns a random integer from 0 to 2^32-1"""
        cls.seed = (cls.A * cls.seed + cls.C) % cls.MOD
        return cls.seed >> 16

    @classmethod
    def randint(cls, lo, hi):
        """Returns a random integer from `lo` to `hi` inclusive on both ends."""
        return (cls.random() % (hi - lo + 1)) + lo

    @classmethod
    def random_chance(cls, ratio):
        """Returns random()/2^32 < ratio"""
        return cls.random()/(1 << 32) < ratio

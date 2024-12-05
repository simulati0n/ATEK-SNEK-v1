import random

class FactManager:
    def __init__(self):
        self.facts = [
            ("Snakes smell with their tongues.", True),
            ("All snakes are venomous.", False),
            ("Snakes have no bones.", False),
            ("Snakes can grow up to 30 feet in length.", True),
            ("Snakes lay eggs, but some give live birth.", True),
            ("In python, the spacing of your code does not matter.",False),
        ]

    def get_random_fact(self):
        return random.choice(self.facts)

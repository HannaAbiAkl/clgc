import sys
sys.path.append('../')
from src.clgc.__base import *
import unittest

class TestSyllogismCategories(unittest.TestCase):
    def test_nl_categorical_syllogism(self):
        test_syllogism = FOLSyllogism("There are no bikes that can be called cars. It is also true that every bike is a type of vehicle. This has led to the conclusion that a portion of vehicles are bikes.")
        self.assertEqual(test_syllogism.categorize(), "categorical")

    def test_nl_hypothetical_syllogism(self):
        test_syllogism = FOLSyllogism("Every single river is a thing that flows towards the sea. The Amazon River is a river. A number of parts of the Amazon River flow towards the sea.")
        self.assertEqual(test_syllogism.categorize(), "hypothetical")

    def test_fol_categorical_syllogism(self):
        test_syllogism = FOLSyllogism("∀x (Bikes(x) → ¬Calledcars(x)) ∀x (Bike(x) → Vehicle(x)) ∃x (Vehicles(x) ∧ Bikes(x))")
        self.assertEqual(test_syllogism.categorize(), "categorical")

    def test_fol_hypothetical_syllogism(self):
        test_syllogism = FOLSyllogism("∀x (River(x) → Thingflowstowardssea(x)) ∀x (Amazonriver(x) → River(x)) ∃x (Amazonriver(x) → Thingflowstowardssea(x))")
        self.assertEqual(test_syllogism.categorize(), "hypothetical")

if __name__ == '__main__':
    unittest.main()
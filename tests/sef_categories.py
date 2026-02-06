import sys
sys.path.append('../')
from src.clgc.logic import categorize_syllogism
import unittest

class TestSyllogismCategories(unittest.TestCase):
    def test_nl_categorical_syllogism(self):
        self.assertEqual(categorize_syllogism("There are no bikes that can be called cars. It is also true that every bike is a type of vehicle. This has led to the conclusion that a portion of vehicles are bikes."), "categorical")

    def test_nl_hypothetical_syllogism(self):
        self.assertEqual(categorize_syllogism("Every single river is a thing that flows towards the sea. The Amazon River is a river. A number of parts of the Amazon River flow towards the sea."), "hypothetical")

    def test_fol_categorical_syllogism(self):
        self.assertEqual(categorize_syllogism("∀x (Bikes(x) → ¬Calledcars(x)) ∀x (Bike(x) → Vehicle(x)) ∃x (Vehicles(x) ∧ Bikes(x))"), "categorical")

    def test_fol_hypothetical_syllogism(self):
        self.assertEqual(categorize_syllogism("∀x (River(x) → Thingflowstowardssea(x)) ∀x (Amazonriver(x) → River(x)) ∃x (Amazonriver(x) → Thingflowstowardssea(x))"), "hypothetical")

if __name__ == '__main__':
    unittest.main()
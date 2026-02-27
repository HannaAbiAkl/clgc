import sys
sys.path.append('../')
from src.clgc.__base import *
import unittest

class TestFolTransformations(unittest.TestCase):
    def test_add_statements(self):
        test_syllogism = FOLSyllogism("∃x (Canine(x) ∧ ¬AquaticCreatureKnownAsFish(x))\n")
        test_syllogism.add_statements(["∀x (Fish(x) → ¬MammalThereforeEveryCanineFallUnderTheCategoryOfMammal(x))\n"])  
        self.assertEqual(test_syllogism.statements, ["∃x (Canine(x) ∧ ¬AquaticCreatureKnownAsFish(x))", "∀x (Fish(x) → ¬MammalThereforeEveryCanineFallUnderTheCategoryOfMammal(x))"])

    def test_add_premises(self):
        test_syllogism = FOLSyllogism("∃x (Canine(x) ∧ ¬AquaticCreatureKnownAsFish(x))\n ∀x (Bike(x) → Vehicle(x))\n")
        test_syllogism.add_premises(["∀x (Fish(x) → ¬MammalThereforeEveryCanineFallUnderTheCategoryOfMammal(x))\n"])  
        self.assertEqual(test_syllogism.premises, ["∃x (Canine(x) ∧ ¬AquaticCreatureKnownAsFish(x))", "∀x (Fish(x) → ¬MammalThereforeEveryCanineFallUnderTheCategoryOfMammal(x))"])

    def test_add_conclusion(self):
        test_syllogism = FOLSyllogism("∃x (Canine(x) ∧ ¬AquaticCreatureKnownAsFish(x))\n ∀x (Bike(x) → Vehicle(x))\n")
        test_syllogism.add_conclusion("∀x (Fish(x) → ¬MammalThereforeEveryCanineFallUnderTheCategoryOfMammal(x))\n")  
        self.assertEqual(test_syllogism.conclusion, "∀x (Fish(x) → ¬MammalThereforeEveryCanineFallUnderTheCategoryOfMammal(x))")

if __name__ == '__main__':
    unittest.main()
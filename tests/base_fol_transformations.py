import sys
sys.path.append('../')
from src.clgc.__base import *
import unittest

class TestFolTransformations(unittest.TestCase):
    def test_fol_to_minifol(self):
        test_syllogism = FOLSyllogism("∀x (BelieveIn(x, santaClaus) ⊕ ThinkMadeUp(x, santaClaus))").syllogism
        self.assertEqual(FOLSyllogism.fol_to_minifol(test_syllogism), "all:x (believein(x, santaclaus) ^ thinkmadeup(x, santaclaus))")

    def test_fol_to_minifol2(self):
        test_syllogism = FOLSyllogism("∃x (Canine(x) ∧ ¬AquaticCreatureKnownAsFish(x))\n ∀x (Fish(x) → ¬MammalThereforeEveryCanineFallUnderTheCategoryOfMammal(x))\n").syllogism
        self.assertEqual(FOLSyllogism.fol_to_minifol2(test_syllogism), "x (canine(x) & ~aquaticcreatureknownasfish(x))\n all:x (fish(x) :- ~mammalthereforeeverycaninefallunderthecategoryofmammal(x))\n")

    def test_fol_to_clif(self):
        test_syllogism = FOLSyllogism("∃x (Canine(x) ∧ ¬AquaticCreatureKnownAsFish(x))\n ∀x (Fish(x) → ¬MammalThereforeEveryCanineFallUnderTheCategoryOfMammal(x))\n").syllogism
        self.assertEqual(FOLSyllogism.fol_to_clif(test_syllogism), "exists x (canine(x) and not aquaticcreatureknownasfish(x))\n forall x (fish(x) implies not mammalthereforeeverycaninefallunderthecategoryofmammal(x))\n")

    def test_fol_to_cgif(self):
        test_syllogism = FOLSyllogism("∃x (Canine(x) ∧ ¬AquaticCreatureKnownAsFish(x))\n ∀x (Fish(x) → ¬MammalThereforeEveryCanineFallUnderTheCategoryOfMammal(x))\n").syllogism
        self.assertEqual(FOLSyllogism.fol_to_cgif(test_syllogism), "[*x [(canine[(?x)]  ~aquaticcreatureknownasfish[(?x)])]\n @every *x [(fish[(?x)]  ~mammalthereforeeverycaninefallunderthecategoryofmammal[(?x)])]\n]")

    def test_fol_to_clingo(self):
        test_syllogism = FOLSyllogism("∃x (Canine(x) ∧ ¬AquaticCreatureKnownAsFish(x))\n ∀x (Fish(x) → ¬MammalThereforeEveryCanineFallUnderTheCategoryOfMammal(x))\n").syllogism
        self.assertEqual(FOLSyllogism.fol_to_clingo(test_syllogism), " (canine(x) , notaquaticcreatureknownasfish(x))\n forall (fish(x) -: notmammalthereforeeverycaninefallunderthecategoryofmammal(x))\n")

    def test_fol_to_tflplus(self):
        test_syllogism = FOLSyllogism("∃x (Canine(x) ∧ ¬AquaticCreatureKnownAsFish(x))\n ∀x (Fish(x) → ¬MammalThereforeEveryCanineFallUnderTheCategoryOfMammal(x))\n").syllogism
        self.assertEqual(FOLSyllogism.fol_to_tfl_plus(test_syllogism), "+(+C1+-+A1)-(+F0--+M0)")

    def test_fol_to_tfl(self):
        test_syllogism = FOLSyllogism("∃x (Canine(x) ∧ ¬AquaticCreatureKnownAsFish(x))\n").syllogism
        self.assertEqual(FOLSyllogism.fol_to_tfl(test_syllogism), "++C1+-+A1")

    def test_fol_syntax(self):
           test_string = FOLSyllogism("""∃x (Canine(x) ∧ ¬AquaticCreatureKnownAsFish(x))\n""")
           try:
            test_string.validate()
           except Exception as e:
            self.fail(f"Failed to parse FOL string: {e}")

    def test_prolog_syntax(self):
            test_list = ["likes(noor, sausage)",
            "likes(melissa, pasta)",
            "likes(dmitry, cookie)",
            "likes(nikita, sausage)",
            "likes(assel, limonade)",
            "food_type(gouda, cheese)",
            "food_type(ritz, cracker)",
            "food_type(steak, meat)",
            "food_type(sausage, meat)",
            "food_type(limonade, juice)",
            "food_type(cookie, dessert)",
            "flavor(sweet, dessert)",
            "flavor(savory, meat)",
            "flavor(savory, cheese)",
            "flavor(sweet, juice)",
            "food_flavor(X, Y) :- food_type(X, Z), flavor(Y, Z)",
            "dish_to_like(X, Y) :- likes(X, L), food_type(L, T), flavor(F, T), food_flavor(Y, F), neq(L, Y)"]
            for statement in test_list:
                prolog_syllogism = FOLSyllogism(statement + " .\n")
                try:
                    prolog_syllogism.validate(grammar='PROLOG')
                except Exception as e:
                    self.fail(f"Failed to parse Prolog string: {e}")   

if __name__ == '__main__':
    unittest.main()
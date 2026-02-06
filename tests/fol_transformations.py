import sys
sys.path.append('../')
from src.clgc.logic import fol_to_minifol, fol_to_minifol2, fol_to_clif, fol_to_cgif, fol_to_clingo, fol_to_tfl_plus, fol_to_tfl, run_program, PARSER
import unittest

class TestFolTransformations(unittest.TestCase):
    def test_fol_to_minifol(self):
        self.assertEqual(fol_to_minifol("∀x (BelieveIn(x, santaClaus) ⊕ ThinkMadeUp(x, santaClaus))"), "all:x (believein(x, santaclaus) ^ thinkmadeup(x, santaclaus))")

    def test_fol_to_minifol2(self):
        self.assertEqual(fol_to_minifol2("∃x (Canine(x) ∧ ¬AquaticCreatureKnownAsFish(x))\n ∀x (Fish(x) → ¬MammalThereforeEveryCanineFallUnderTheCategoryOfMammal(x))\n"), "x (canine(x) & ~aquaticcreatureknownasfish(x))\n all:x (fish(x) :- ~mammalthereforeeverycaninefallunderthecategoryofmammal(x))\n")

    def test_fol_to_clif(self):
        self.assertEqual(fol_to_clif("∃x (Canine(x) ∧ ¬AquaticCreatureKnownAsFish(x))\n ∀x (Fish(x) → ¬MammalThereforeEveryCanineFallUnderTheCategoryOfMammal(x))\n"), "exists x (canine(x) and not aquaticcreatureknownasfish(x))\n forall x (fish(x) implies not mammalthereforeeverycaninefallunderthecategoryofmammal(x))\n")

    def test_fol_to_cgif(self):
        self.assertEqual(fol_to_cgif("∃x (Canine(x) ∧ ¬AquaticCreatureKnownAsFish(x))\n ∀x (Fish(x) → ¬MammalThereforeEveryCanineFallUnderTheCategoryOfMammal(x))\n"), "[*x [(canine[(?x)]  ~aquaticcreatureknownasfish[(?x)])]\n @every *x [(fish[(?x)]  ~mammalthereforeeverycaninefallunderthecategoryofmammal[(?x)])]\n]")

    def test_fol_to_clingo(self):
        self.assertEqual(fol_to_clingo("∃x (Canine(x) ∧ ¬AquaticCreatureKnownAsFish(x))\n ∀x (Fish(x) → ¬MammalThereforeEveryCanineFallUnderTheCategoryOfMammal(x))\n"), " (canine(x) , notaquaticcreatureknownasfish(x))\n forall (fish(x) -: notmammalthereforeeverycaninefallunderthecategoryofmammal(x))\n")

    def test_fol_to_tflplus(self):
        self.assertEqual(fol_to_tfl_plus("∃x (Canine(x) ∧ ¬AquaticCreatureKnownAsFish(x))\n ∀x (Fish(x) → ¬MammalThereforeEveryCanineFallUnderTheCategoryOfMammal(x))\n"), "+(+C1+-+A1)-(+F0--+M0)")

    def test_fol_to_tfl(self):
        self.assertEqual(fol_to_tfl("∃x (Canine(x) ∧ ¬AquaticCreatureKnownAsFish(x))\n"), "++C1+-+A1")

    def test_fol_syntax(self):
           fol_string = """∃x (Canine(x) ∧ ¬AquaticCreatureKnownAsFish(x))\n"""
           try:
            run_program(PARSER, fol_string)
           except Exception as e:
            self.fail(f"Failed to parse FOL string: {e}")

if __name__ == '__main__':
    unittest.main()
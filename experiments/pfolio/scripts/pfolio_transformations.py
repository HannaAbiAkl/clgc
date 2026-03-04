import clgc
from clgc.__base import *

test_syllogism = FOLSyllogism("∀x (WildTurkey(x) → (EasternWildTurkey(x) ∨ OsceolaWildTurkey(x) ∨ GouldsWildTurkey(x) ∨ MerriamsWildTurkey(x) ∨ RiograndeWildTurkey(x) ∨ OcellatedWildTurkey(x)))\n ¬(EasternWildTurkey(tom))\n ¬(OsceolaWildTurkey(tom))\n ¬(GouldsWildTurkey(tom))\n ¬(MerriamsWildTurkey(tom) ∨ RiograndeWildTurkey(tom))\n WildTurkey(tom)\n")
tfl_plus_syllogism = FOLSyllogism.fol_to_tfl_plus(test_syllogism.syllogism)
print("Original FOL Syllogism:", test_syllogism.syllogism)
print("TFL+ Syllogism:", tfl_plus_syllogism)
import sys
sys.path.append('../')
from src.clgc.__base import *

syllogism = FOLSyllogism("∃x (Canine(x) ∧ ¬AquaticCreatureKnownAsFish(x))\n")
#syllogism = FOLSyllogism("LargeComplex(shafaq-asiman) ∧ LargeComplex(shafaq-asiman) ∧ Offshore(shafaq-asiman) ∧ GeologicalStructures(shafaq-asiman) ∧ In(shafaq-asiman, caspiansea)\nNorthwestOf(baku, shafaq-asiman)\n ∀x ∀y (NorthwestOf(x, y) → SoutheastOf(y, x))\n")

# test for clif
clif_syllogism = FOLSyllogism.fol_to_clif(syllogism.syllogism)
#print("*** CLIF STRING:", clif_syllogism)
#print("*** Output CLIF json format ***")
json_clif = FOLSyllogism.treeify(clif_syllogism, grammar="clif", format="json")
#print(json_clif)
#print("*** Output simplified CLIF AST ***")
#print(simplify_tree(json_clif))
print("*** Output TOON CLIF ***")
print(FOLSyllogism.toonify(FOLSyllogism.simplify_tree(json_clif)))

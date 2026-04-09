import sys
sys.path.append('../')
from src.clgc.__base import *

syllogism = FOLSyllogism("∃x (Canine(x) ∧ ¬AquaticCreatureKnownAsFish(x))\n")
# test output tree format
print("*** Output FOL tree format ***")
print(FOLSyllogism.treeify(syllogism.syllogism))
# test output str format
print("*** Output FOL str format ***")
print(FOLSyllogism.treeify(syllogism.syllogism, format="str"))
# test output json format
print("*** Output FOL json format ***")
print(FOLSyllogism.treeify(syllogism.syllogism, format="json"))

# test for tfl/tfl+
tfl_plus_syllogism = FOLSyllogism.fol_to_tfl_plus(syllogism.syllogism)
print("*** TFL+ STRING:", tfl_plus_syllogism)
FOLSyllogism(tfl_plus_syllogism+'\n').validate(grammar='tfl+')
print("*** Output TFL+ tree format ***")
print(FOLSyllogism.treeify(tfl_plus_syllogism, grammar="tfl+", format="tree"))
print("*** Output TFL+ str format ***")
print(FOLSyllogism.treeify(tfl_plus_syllogism, grammar="tfl+", format="str"))
print("*** Output TFL+ json format ***")
print(FOLSyllogism.treeify(tfl_plus_syllogism, grammar="tfl+", format="json"))

# test for clif
clif_syllogism = FOLSyllogism.fol_to_clif(syllogism.syllogism)
print("*** CLIF STRING:", clif_syllogism)
FOLSyllogism(clif_syllogism+'\n').validate(grammar='clif')
print("*** Output CLIF tree format ***")
print(FOLSyllogism.treeify(clif_syllogism, grammar="clif", format="tree"))
print("*** Output CLIF str format ***")
print(FOLSyllogism.treeify(clif_syllogism, grammar="clif", format="str"))
print("*** Output CLIF json format ***")
print(FOLSyllogism.treeify(clif_syllogism, grammar="clif", format="json"))

# test for cgif
cgif_syllogism = FOLSyllogism.fol_to_cgif(syllogism.syllogism)
print("*** CGIF STRING:", cgif_syllogism)
FOLSyllogism(cgif_syllogism+'\n').validate(grammar='cgif')
print("*** Output CGIF tree format ***")
print(FOLSyllogism.treeify(cgif_syllogism, grammar="cgif", format="tree"))
print("*** Output CGIF str format ***")
print(FOLSyllogism.treeify(cgif_syllogism, grammar="cgif", format="str"))
print("*** Output CGIF json format ***")
print(FOLSyllogism.treeify(cgif_syllogism, grammar="cgif", format="json"))

# test for minifol2
minifol2_syllogism = FOLSyllogism.fol_to_minifol2(syllogism.syllogism)
print("*** MINIFOL2 STRING:", minifol2_syllogism)
FOLSyllogism(minifol2_syllogism +'\n').validate(grammar='minifol2')
print("*** Output MINIFOL2 tree format ***")
print(FOLSyllogism.treeify(minifol2_syllogism, grammar="minifol2", format="tree"))
print("*** Output MINIFOL2 str format ***")
print(FOLSyllogism.treeify(minifol2_syllogism, grammar="minifol2", format="str"))
print("*** Output MINIFOL2 json format ***")
print(FOLSyllogism.treeify(minifol2_syllogism, grammar="minifol2", format="json"))


# test for clingo
clingo_syllogism = FOLSyllogism.fol_to_clingo(syllogism.syllogism)
print("*** CLINGO STRING:", clingo_syllogism)
FOLSyllogism(clingo_syllogism +'\n').validate(grammar='clingo')
print("*** Output CLINGO tree format ***")
print(FOLSyllogism.treeify(clingo_syllogism, grammar="clingo", format="tree"))
print("*** Output CLINGO str format ***")
print(FOLSyllogism.treeify(clingo_syllogism, grammar="clingo", format="str"))
print("*** Output CLINGO json format ***")
print(FOLSyllogism.treeify(clingo_syllogism, grammar="clingo", format="json"))

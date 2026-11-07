import sys
sys.path.append('../')
from src.clgc.__base import *

test_syllogism = FOLSyllogism("∀x (Tiger(x) → Cat(x))\n∀x (Cat(x) → ¬Dog(x))\n∀x (BengalTiger(x) → Tiger(x))\n∀x (Husky(x) → Dog(x))\nBengalTiger(fido) ⊕ Cat(fido)\n")
test_syllogism.add_conclusion("Husky(fido)")
# test fol to graph
fol_syllogism_graph = FOLSyllogism.ast_to_syllogism_graph(test_syllogism.syllogism+'\n')
print("Syllogism Graph:")
print(fol_syllogism_graph)
# plot the graph using PyVis
FOLSyllogism.plot_syllogism_pyvis(fol_syllogism_graph, output_filename="fol_syllogism_graph.html")


# test for clif
clif_syllogism = FOLSyllogism.fol_to_clif(test_syllogism.syllogism)
print("CLIF Representation of the Syllogism:")
print(clif_syllogism)
# test clif to graph
syllogism_graph = FOLSyllogism.ast_to_syllogism_graph(clif_syllogism+'\n', grammar="clif")
print("Syllogism Graph:")
print(syllogism_graph)
# plot the graph using PyVis
FOLSyllogism.plot_syllogism_pyvis(syllogism_graph, output_filename="test_syllogism_graph.html")

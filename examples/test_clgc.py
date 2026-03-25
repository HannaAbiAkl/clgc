import sys
sys.path.append('../')
from src.clgc.__base import *

# test SEF categoirization
syllogism = "∀x (Bikes(x) → ¬Calledcars(x))\n ∀x (Bike(x) → Vehicle(x))\n ∃x (Vehicles(x) ∧ Bikes(x))\n"
print(categorize_syllogism(syllogism))

# test FOL to TFL+ translation
tfl_syllogism = fol_to_tfl_plus(syllogism)
print(tfl_syllogism)
from clgc.__base import *

# test SEF categoirization
syllogism = FOLSyllogism("∀x (Bikes(x) → ¬Calledcars(x))\n ∀x (Bike(x) → Vehicle(x))\n ∃x (Vehicles(x) ∧ Bikes(x))\n")
print(syllogism.categorize())

# get syllogism as text
test_syllogism = FOLSyllogism("∀x (Bikes(x) → ¬Calledcars(x))\n ∀x (Bike(x) → Vehicle(x))\n ∃x (Vehicles(x) ∧ Bikes(x))\n").syllogism
# convert to desired logical notation - here TFL+
tfl_plus_syllogism = FOLSyllogism.fol_to_tfl_plus(test_syllogism)
print("*** TFL+:", tfl_plus_syllogism)
import sys
sys.path.append('../')
from src.clgc.__base import *

# test SEF categoirization
syllogism = FOLSyllogism("∀x (Bikes(x) → ¬Calledcars(x))\n ∀x (Bike(x) → Vehicle(x))\n ∃x (Vehicles(x) ∧ Bikes(x))\n")
print(syllogism.categorize())

# get syllogism as text
test_syllogism = FOLSyllogism("∀x (Bikes(x) → ¬Calledcars(x))\n ∀x (Bike(x) → Vehicle(x))\n ∃x (Vehicles(x) ∧ Bikes(x))\n").syllogism
# convert to desired logical notation - here TFL+
tfl_plus_syllogism = FOLSyllogism.fol_to_tfl_plus(test_syllogism)
print("*** TFL+:", tfl_plus_syllogism)

# test validation on alternative grammar (Prolog)
prolog_list = ["likes(noor, sausage)",
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
for statement in prolog_list:
    prolog_syllogism = FOLSyllogism(statement + " .\n")
    prolog_syllogism.validate(grammar='PROLOG')

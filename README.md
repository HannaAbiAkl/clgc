![alt text for screen readers](https://raw.githubusercontent.com/hannaabiakl/clgc/main/logo.png "CLGC")

# CLGC

A Python package to translate First-Order Logic (FOL) into different knowledge representation languages

## Scope

A package used for handling logic statements and logic analysis using formal knowledge representation languages.

## Key Features
- Translate FOL statements to other formal Knowledge Representation (KR) languages
- Categorize syllogisms by type

## Supported KR Languages
- Common Logic Interchange Format (CLIF)
- Conceptual Graph Interchange Format (CGIF)
- Tensor Function Logic (TFL)
- Tensor Function Logic Plus (TFL+)
- CLINGO
- MINIFOLX
- PROLOG

## Setup
Start by installing the package

`pip install clgc`

Then install the dependencies

`pip install -r requirements.txt`

## Basic Usage
To load all functionalities

`from clgc.__base import *`

To create a valid syllogism in FOL, each statement of the syllogism should be followed by the `'\n'` terminator. The following example creates a syllogism of 2 premises and a conclusion:

```python
syllogism = FOLSyllogism("∀x (Bikes(x) → ¬Calledcars(x))\n ∀x (Bike(x) → Vehicle(x))\n ∃x (Vehicles(x) ∧ Bikes(x))\n")
```

To categorize syllogisms in natural language or first-order language

```python
syllogism = FOLSyllogism("∀x (Bikes(x) → ¬Calledcars(x))\n ∀x (Bike(x) → Vehicle(x))\n ∃x (Vehicles(x) ∧ Bikes(x))\n")

print
(syllogism.categorize())
# categorical
```

To translate from first-order language to another language (here, TFL+)

```python
# get syllogism as text
test_syllogism = FOLSyllogism("∀x (Bikes(x) → ¬Calledcars(x))\n ∀x (Bike(x) → Vehicle(x))\n ∃x (Vehicles(x) ∧ Bikes(x))\n").syllogism
# convert to desired logical notation - here TFL+
tfl_plus_syllogism = FOLSyllogism.fol_to_tfl_plus(test_syllogism)

print(tfl_syllogism)
# -(+B0--+C0)-(+B0-+V0)+(+V1++B1)
```

A list of functions are available to modify a syllogism:
- `add_statements` (automatically adds the given statements in that order meaning the last given statement becomes the conclusion of the syllogism)
- `add_premises` (automatically keeps the original conclusion and adds everything given as premises)
- `add_conclusion` (automatically takes the given statement as the conclusion and renders everything else to premises)

An example of adding new statements

```python
test_syllogism = FOLSyllogism("∃x (Canine(x) ∧ ¬AquaticCreatureKnownAsFish(x))\n")
        test_syllogism.add_statements(["∀x (Fish(x) → ¬MammalThereforeEveryCanineFallUnderTheCategoryOfMammal(x))\n"])   

print(test_syllogism.statements)
# ["∃x (Canine(x) ∧ ¬AquaticCreatureKnownAsFish(x))", "∀x (Fish(x) → ¬MammalThereforeEveryCanineFallUnderTheCategoryOfMammal(x))"])
```

An example of adding new premises

```python
test_syllogism = FOLSyllogism("∃x (Canine(x) ∧ ¬AquaticCreatureKnownAsFish(x))\n ∀x (Bike(x) → Vehicle(x))\n")
        test_syllogism.add_premises(["∀x (Fish(x) → ¬MammalThereforeEveryCanineFallUnderTheCategoryOfMammal(x))\n"]) 

print(test_syllogism.premises)
# ["∃x (Canine(x) ∧ ¬AquaticCreatureKnownAsFish(x))", "∀x (Fish(x) → ¬MammalThereforeEveryCanineFallUnderTheCategoryOfMammal(x))"]
```

An example of adding a new conclusion

```python
test_syllogism = FOLSyllogism("∃x (Canine(x) ∧ ¬AquaticCreatureKnownAsFish(x))\n ∀x (Bike(x) → Vehicle(x))\n")
        test_syllogism.add_conclusion("∀x (Fish(x) → ¬MammalThereforeEveryCanineFallUnderTheCategoryOfMammal(x))\n") 

print(test_syllogism.conclusion)
# "∀x (Fish(x) → ¬MammalThereforeEveryCanineFallUnderTheCategoryOfMammal(x))"
```

## Integration
As CLGC manipulates logical notations, it can be integrated with other logic programming libraries.
### Pytholog
The example below is adapted from Pytholog [[1]](#ref-1) to show how CLGC objects can be leveraged to write and validate correct logical programming notations like PROLOG.

**<ins>_Note:</ins> You should make sure to install the dependencies of the target library integrations._**

```python
import pytholog as pl
from clgc.__base import *

clgc_kb = pl.KnowledgeBase("clgc_flavor")
clgc_list = ["likes(noor, sausage)",
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
# validate if every fact in the list is in prolog
# if so, add it to the db
# if not, interrupt the program
for statement in clgc_list:
    prolog_syllogism = FOLSyllogism(statement + " .\n")
    try:
        prolog_syllogism.validate(grammar='PROLOG')
    except Exception as e:
        raise Exception(f"Failed to parse Prolog string: {e}")

# now everything that is added is valid
clgc_kb(clgc_list)

# query the db in clgc
query_str = "likes(noor, sausage)"
query = FOLSyllogism(statement + " .\n")
# check if query is valid
# if yes, query the db for an answer
# if not, interrupt the program
try:
    query.validate(grammar='PROLOG')
    print(clgc_kb.query(pl.Expr(query_str)))
except Exception as e:
    raise Exception(f"Failed to parse Prolog string: {e}")
# ['Yes']
```

## References
1. <span id=ref-1>MNoorFawi. (n.d.). GitHub - MNoorFawi/pytholog: Python library that enables using prolog syntax and logic programming in python. GitHub. [[code]](https://github.com/MNoorFawi/pytholog/tree/master?tab=readme-ov-file)</span>
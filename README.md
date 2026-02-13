![alt text for screen readers](logo.png "CLGC")

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

## Setup
Start by installing the package

`pip install -i https://test.pypi.org/simple/ clgc==0.0.1`

Then install the dependencies

`pip install -r requirements.txt`

## Basic Usage
To load all functionalities

`from clgc.logic import *`

To categorize syllogisms in natural language or first-order language

```python
syllogism = "∀x (Bikes(x) → ¬Calledcars(x))\n ∀x (Bike(x) → Vehicle(x))\n ∃x (Vehicles(x) ∧ Bikes(x))\n"

print
(categorize_syllogism(syllogism))
# categorical
```

To translate from first-order language to another language (here, TFL+)

```python
tfl_syllogism = fol_to_tfl_plus(syllogism)

print(tfl_syllogism)
# -(+B0--+C0)-(+B0-+V0)+(+V1++B1)
```
import pytholog as pl
from clgc.__base import *

# test raw pytholog
new_kb = pl.KnowledgeBase("flavor")
new_kb(["likes(noor, sausage)",
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
        "dish_to_like(X, Y) :- likes(X, L), food_type(L, T), flavor(F, T), food_flavor(Y, F), neq(L, Y)"])

print(new_kb.query(pl.Expr("likes(noor, sausage)")))
# ['Yes']

# now integrate clgc to manipulate objects
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
# if not, remove it from the list
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
try:
    query.validate(grammar='PROLOG')
    print(clgc_kb.query(pl.Expr(query_str)))
except Exception as e:
    raise Exception(f"Failed to parse Prolog string: {e}")

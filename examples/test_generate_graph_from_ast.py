import pandas as pd
import json
import matplotlib.pyplot as plt
import networkx as nx
import test_ast_to_graph as ast_graph

# Complete structural AST JSON dataset matching your exact structure
dataset_df = pd.read_csv(f"../experiments/pfolio/data/pfolio_fol_ast_test.csv")

# test on first instance of pfolio syllogism

premises_ast = dataset_df["Premises - FOL"].iloc[1]
conclusion_ast = dataset_df["Conclusions - FOL"].iloc[1]
# replace single quotes with double quotes to make it valid JSON
premises_ast = premises_ast.replace("'", '"')
conclusion_ast = conclusion_ast.replace("'", '"')
# add conlusion as a child to premises dict
premises_ast = json.loads(premises_ast)
conclusion_ast = json.loads(conclusion_ast)
premises_ast["children"].append(conclusion_ast["children"][0]["children"][0])
premises_ast = premises_ast["children"][0]  # get the first child of premises as the root of the AST
ast_data = premises_ast
print(ast_data)

# generate graph from AST
G = ast_graph.ast_to_syllogism_graph(ast_data)
ast_graph.plot_syllogism_pyvis(G)
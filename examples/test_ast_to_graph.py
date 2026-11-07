import json
from sys import prefix
import matplotlib.pyplot as plt
import networkx as nx
from pyvis.network import Network
import pandas as pd

# Complete structural AST JSON dataset matching your exact structure
dataset_df = pd.read_csv(f"../experiments/folio/data/folio_ast_test.csv")
premises_ast = dataset_df["Premises - CLIF"].iloc[36]
conclusion_ast = dataset_df["Conclusions - CLIF"].iloc[36]
# replace single quotes with double quotes to make it valid JSON
premises_ast = premises_ast.replace("'", '"')
conclusion_ast = conclusion_ast.replace("'", '"')
# add conlusion as a child to premises dict
premises_ast = json.loads(premises_ast)
conclusion_ast = json.loads(conclusion_ast)
premises_ast["children"].append(conclusion_ast["children"][0]["children"][0])
premises_ast = premises_ast["children"][0]  # get the first child of premises as the root of the AST
ast_data = premises_ast

def extract_text(node):
    """Recursively processes specific sub-tokens to rebuild logic strings."""
    pieces = []
    if "text" in node:
        pieces.append(node["text"])
    if "children" in node:
        for child in node["children"]:
            pieces.extend(extract_text(child))
    return "".join(pieces)

def clean_syntax(text):
    """Formats string operations into formal math notation markers."""
    return (text.strip()
            .replace("forall", "∀ ")
            .replace("implies", " → ")
            .replace("and", " ∧ ")
            .replace("not", " ¬ ")
            .replace("()", ""))


def ast_to_syllogism_graph(ast_dict):
  """Transforms an AST into a directed NetworkX graph where all nodes

  sharing the same name/label (regardless of type, e.g., symbol 'x' and term 'x')
  are merged into a single unique node, accumulating all incoming and
  outgoing edges.
  """
  G = nx.DiGraph()

  # 1. Add Root Node
  root_node = "Syllogism"
  G.add_node(root_node, label="Syllogism", node_type="root")

  # Helper to safely locate statements in the AST structure
  def find_statements(node):
    stats = []
    if not isinstance(node, dict):
      return stats

    if node.get("type") == "stat":
      stats.append(node)

    for child in node.get("children", []):
      stats.extend(find_statements(child))

    return stats

  statements = find_statements(ast_dict)
  if not statements:
    return G

  premises = statements[:-1]
  conclusion = statements[-1]

  # Helper to split a term node's contents by commas (e.g., x,y or tecmo,japan)
  def extract_sub_terms_from_node(node):
    if not isinstance(node, dict):
      return []

    sub_terms = []
    current_letters = []
    for child in node.get("children", []):
      child_type = child.get("type")
      if child_type == "COMMA":
        if current_letters:
          sub_terms.append("".join(current_letters))
          current_letters = []
      elif child_type == "LETTER" and "text" in child:
        current_letters.append(child["text"])
      else:
        nested = extract_sub_terms_from_node(child)
        if nested:
          sub_terms.extend(nested)
    if current_letters:
      sub_terms.append("".join(current_letters))

    if not sub_terms and "text" in node:
      sub_terms.append(node["text"])

    return sub_terms

  # Helper to find text inside simple nodes like quantifier, keyword, symbol
  def get_node_text(node):
    if not isinstance(node, dict):
      return ""
    if "text" in node:
      return node["text"]
    for child in node.get("children", []):
      res = get_node_text(child)
      if res:
        return res
    return ""

  def collect_keywords(node, keywords):
    if not isinstance(node, dict):
      return
    if node.get("type") == "keyword":
      kw_text = get_node_text(node)
      if kw_text and kw_text not in keywords:
        keywords.append(kw_text)
    for child in node.get("children", []):
      collect_keywords(child, keywords)

  def find_atomic_propositions(node):
    aps = []
    if not isinstance(node, dict):
      return aps
    if node.get("type") == "atomicproposition":
      aps.append(node)
    for child in node.get("children", []):
      aps.extend(find_atomic_propositions(child))
    return aps

  # Helper to ensure unique nodes by label name (merges different types with same name)
  def add_merged_node(label, node_type):
    if not G.has_node(label):
      G.add_node(label, label=label, node_type=node_type)
    else:
      # Optional: update node_type to reflect multiple roles if needed
      existing_type = G.nodes[label].get("node_type", "")
      if node_type not in existing_type:
        G.nodes[label]["node_type"] = f"{existing_type},{node_type}"
    return label

  # Process a single statement (Premise or Conclusion)
  def process_statement(stat_node, parent_graph_node):
    quantifier_label = None
    symbol_label = None

    def find_quantifier_symbol(node):
      nonlocal quantifier_label, symbol_label
      if not isinstance(node, dict):
        return
      ntype = node.get("type")
      if ntype == "quantifier":
        q_text = get_node_text(node)
        if q_text:
          quantifier_label = add_merged_node(q_text, "quantifier")
          G.add_edge(parent_graph_node, quantifier_label)
      elif ntype == "symbol" and quantifier_label:
        s_text = get_node_text(node)
        if s_text:
          symbol_label = add_merged_node(s_text, "symbol")
          G.add_edge(quantifier_label, symbol_label)

      for child in node.get("children", []):
        find_quantifier_symbol(child)

    find_quantifier_symbol(stat_node)

    # Process Atomic Propositions (Predicate -> Argument Term Edges)
    aps = find_atomic_propositions(stat_node)
    statement_terms = set()

    for ap in aps:
      term_children = [
          c for c in ap.get("children", []) if c.get("type") == "term"
      ]
      ap_terms = []
      for tc in term_children:
        sub = extract_sub_terms_from_node(tc)
        ap_terms.extend(sub)

      if ap_terms:
        predicate_text = ap_terms[0]
        pred_label = add_merged_node(predicate_text, "term")
        G.add_edge(parent_graph_node, pred_label)
        statement_terms.add(predicate_text)

        for arg_text in ap_terms[1:]:
          arg_label = add_merged_node(arg_text, "term")
          G.add_edge(parent_graph_node, arg_label)
          statement_terms.add(arg_text)

          # Directed edge from predicate to argument term
          G.add_edge(pred_label, arg_label)

    # Fallback for any standalone terms not caught in atomic propositions
    def find_all_terms(node):
      if not isinstance(node, dict):
        return
      if node.get("type") == "term":
        for t in extract_sub_terms_from_node(node):
          if t not in statement_terms:
            t_label = add_merged_node(t, "term")
            G.add_edge(parent_graph_node, t_label)
            statement_terms.add(t)
      for child in node.get("children", []):
        find_all_terms(child)

    find_all_terms(stat_node)

    # Keywords -> Connect keyword to all terms in the statement
    keywords = []
    collect_keywords(stat_node, keywords)

    for kw in keywords:
      kw_label = add_merged_node(kw, "keyword")
      G.add_edge(parent_graph_node, kw_label)

      # Connect keyword to all terms present in this statement
      for t in statement_terms:
        G.add_edge(kw_label, t)

  # 2. Process Premises
  for idx, premise in enumerate(premises):
    premise_name = f"Premise_{idx + 1}"
    add_merged_node(premise_name, "premise")
    G.add_edge(root_node, premise_name)
    process_statement(premise, premise_name)

  # 3. Process Conclusion
  conclusion_name = "Conclusion"
  add_merged_node(conclusion_name, "conclusion")
  G.add_edge(root_node, conclusion_name)
  process_statement(conclusion, conclusion_name)

  return G

def plot_syllogism_pyvis(G, output_filename="syllogism_graph.html"):
  """Plots the NetworkX directed graph using PyVis for an interactive

  HTML visualization, coloring nodes by type and keeping custom labels.
  """
  # Initialize PyVis Network (directed=True, notebook=False for standalone script execution)
  net = Network(
      height="750px", width="100%", directed=True, notebook=False, cdn_resources="remote"
  )

  # Color mapping based on node types
  color_map = {
      "root": "#1f77b4",  # Blue
      "premise": "#2ca02c",  # Green
      "conclusion": "#d62728",  # Red
      "quantifier": "#ff7f0e",  # Orange
      "keyword": "#bcbd22",  # Olive / Yellow-green
      "symbol": "#9467bd",  # Purple
      "term": "#aec7e8",  # Light blue
  }

  # Add nodes from NetworkX graph with custom styling and tooltips
  for node_id, data in G.nodes(data=True):
    ntype = data.get("node_type", "term")
    label = data.get("label", node_id)
    color = color_map.get(ntype, "#aec7e8")

    net.add_node(
        node_id,
        label=label,
        title=f"Type: {ntype}<br>ID: {node_id}",
        color=color,
        size=50 if ntype in ["root", "premise", "conclusion"] else 35,
    )

  # Add edges from NetworkX graph
  for u, v in G.edges():
    net.add_edge(u, v, arrows="to", color="#888888")

  # Optional: configure physics layout for clean spacing
  net.barnes_hut(
      gravity=-2000, central_gravity=0.3, spring_length=90
  )

  # Save and generate HTML file
  net.save_graph(output_filename)
  print(f"Interactive graph saved to {output_filename}. Open it in your browser!")


G = ast_to_syllogism_graph(ast_data)
adj_matrix = nx.adjacency_matrix(G)
print("Adjacency Matrix:\n", adj_matrix.todense())
plot_syllogism_pyvis(G)
import json
import sys
import lark
from lark import Lark
import matplotlib.pyplot as plt
import networkx as nx
from pyvis.network import Network

FOL_GRAMMAR = r"""
    start: program
    program: [stat]+
    stat: proposition newline | keyword* quantifier* symbol* leftparen* (quantifier symbol)* proposition rightparen* newline | keyword* (quantifier symbol)* leftparen* (quantifier symbol)* proposition rightparen* newline
    proposition: atomicproposition | complexproposition
    complexproposition: keyword* proposition keyword leftparen* (quantifier symbol)* proposition rightparen*
    atomicproposition: leftparen* term* leftparen* term* rightparen*
    !term: (LETTER+) (LETTER+|DIGIT+|"=" | "+" | "-" | "," | "≠")* | (DIGIT+) (LETTER+|DIGIT+|"=" | "+" | "-" | "," | "≠")*
    !leftparen: "("
    !rightparen: ")"
    !keyword: "∧" | "¬" | "→" | "∨" | "⊕" | "↔" | "⟷"
    !quantifier: "∃" | "∀"
    symbol: LETTER
    newline: /\n/

    %import common.LETTER
    %import common.DIGIT
    %import common.INT -> NUMBER
    %import common.ESCAPED_STRING -> STRING
    %import common.WS
    %ignore WS
"""

TFL_GRAMMAR = r"""
    start: program
    program: [stat]+
    stat: proposition newline
    proposition: atomicproposition | complexproposition
    complexproposition: leftparen proposition rightparen | proposition plus proposition | proposition minus proposition
    atomicproposition: term
    leftparen: "("
    rightparen: ")"
    plus: "+"
    minus: "-"
    term: plus T n | minus T n
    T: LETTER
    n: NUMBER
    newline: /\n/

    %import common.LETTER
    %import common.INT -> NUMBER
    %import common.WS
    %ignore WS
"""

PARSER = Lark(FOL_GRAMMAR)

def run_program(parser, program):
    parse_tree = parser.parse(program)
    for inst in parse_tree.children:
        print("INST:",inst)
        print("************")

# test how to manipulate Lark parse tree output
def tree_to_json_str(item):
    output = []
    tree_to_json(item, output.append)  # will build output in memory
    return ''.join(output)

def tree_to_json(item, write=None):
    """ Writes a Lark tree as a JSON dictionary. """
    if write is None: write = sys.stdout.write
    _tree_to_json(item, write, 0)

def _tree_to_json(item, write, level):
    indent = '  ' * level
    level += 1
    if isinstance(item, lark.Tree):
        write(f'{indent}{{ "type": "{item.data}", "children": [\n')
        sep = ''
        for child in item.children:
            write(indent)
            write(sep)
            _tree_to_json(child, write, level)
            sep = ',\n'
        write(f'{indent}] }}\n')
    elif isinstance(item, lark.Token):
        # reminder: Lark Tokens are directly strings
        # token attrs include: line, end_line, column, end_column, pos_in_stream, end_pos
        write(f'{indent}{{ "type": "{item.type}", "text": "{item}", "line": {item.line}, "col": {item.column} }}\n')
    else:
        assert False, item  # fall-through

# construct TFL from FOL recursively
"""
TFL golden rules:
PLUS: 'yes', 'some', 'is', 'both', 'and', 'then'
MINUS: 'not','every', 'if, 'isn't', 'andn't', 'thenn't'
"""

def construct_tfl_from_fol_json(json_obj, tfl_list):
    for key, value in json_obj.items():
        if isinstance(value, dict):
            construct_tfl_from_fol_json(value, tfl_list)
        elif isinstance(value, list):
            for item in value:
              if isinstance(item, dict):
                if item['type'] == 'quantifier':
                  if item['children'][0]['text'] == "∀":
                    tfl_list.append('-')
                  else:
                    tfl_list.append('+')
                elif item['type'] == 'keyword':
                  # choose PLUS or MINUS sign based on keyword
                  if item['children'][0]['text'] == "∧":
                    tfl_list.append('+')
                  else:
                    tfl_list.append('-')
                elif item['type'] == 'atomicproposition':
                  if item['children']:
                    for elem in item['children']:
                      if elem['type'] == 'term': # verify that we are in the case where there is a literal term in the atomicproposition
                        all_terms = [val['text'] for val in elem['children']]
                        if ',' not in all_terms and len(all_terms) > 1:  # make sure that we are targeting predicates and not terms like (x, y) or (x) or (mike) --> should be flattenShirt for example
                          tfl_list.append('+')
                          tfl_list.append(elem['children'][0]['text'])   # represent predicate by using its first letter, e.g., Recommended(x) --> R
                          tfl_list.append(str(elem['children'][0]['line']))   # in TFL predicates are represented with a letter and a number, e.g., Recommended(x) --> R0
                else:
                  construct_tfl_from_fol_json(item, tfl_list)
        else:
            pass

        #return ''.join(tfl_list)

# construct TFL+ from FOL recursively

"""
TFL+ golden rules:
PLUS: 'yes', 'some', 'is', 'both', 'and', 'then'
MINUS: 'not','every', 'if, 'isn't', 'andn't', 'thenn't'
PARENTHESIS
SUPERSCRIPTS: 0 = FORALL, 1 = MOST, 2 = SOME
"""

def construct_tfl_plus_from_fol_json(json_obj, tfl_list, subscript):
    for key, value in json_obj.items():
        if isinstance(value, dict):
            construct_tfl_plus_from_fol_json(value, tfl_list, subscript)
        elif isinstance(value, list):
            for item in value:
              if isinstance(item, dict):
                if item['type'] == 'quantifier':
                  if item['children'][0]['text'] == "∀":
                    tfl_list.append('-')
                    subscript = 0
                  else:
                    tfl_list.append('+')
                    subscript = 1
                elif item['type'] == 'keyword':
                  # choose PLUS or MINUS sign based on keyword
                  if item['children'][0]['text'] == "∧":
                    tfl_list.append('+')
                  else:
                    tfl_list.append('-')
                elif item['type'] == 'atomicproposition':
                  if item['children']:
                    for elem in item['children']:
                      if elem['type'] == 'term': # verify that we are in the case where there is a literal term in the atomicproposition
                        all_terms = [val['text'] for val in elem['children']]
                        if ',' not in all_terms and len(all_terms) > 1:  # make sure that we are targeting predicates and not terms like (x, y) or (x) or (mike) --> should be flattenShirt for example
                          tfl_list.append('+')
                          tfl_list.append(elem['children'][0]['text'])   # represent predicate by using its first letter, e.g., Recommended(x) --> R
                          tfl_list.append(str(subscript))   # in TFL predicates are represented with a letter and a number, e.g., Recommended(x) --> R0
                      if elem['type'] == 'leftparen':  # keep parenthesis
                        tfl_list.append(elem['children'][0]['text'])
                      if elem['type'] == 'rightparen':
                        tfl_list.append(elem['children'][0]['text'])
                elif item['type'] == 'leftparen':
                  tfl_list.append(item['children'][0]['text'])
                elif item['type'] == 'rightparen':
                  tfl_list.append(item['children'][0]['text'])
                else:
                  construct_tfl_plus_from_fol_json(item, tfl_list, subscript)
        else:
            pass

        #return ''.join(tfl_list)

# test automatic TFL  transformation from FOL
def fol_to_tfl(fol_string):
  print("*** FOL STRING:", fol_string)
  parsed_fol_example = PARSER.parse(fol_string)
  # build JSON string with tree_to_json_str
  json_str_example = tree_to_json_str(parsed_fol_example)
  # now convert to json object
  parsed_json_example = json.loads(json_str_example, strict=False)
  tfl_example = []
  construct_tfl_from_fol_json(parsed_json_example, tfl_example)
  tfl_example_str = ''.join(tfl_example)
  return tfl_example_str


def fol_to_tfl_plus(fol_string):
  print("*** FOL STRING:", fol_string)
  parsed_fol_example = PARSER.parse(fol_string)
  # build JSON string with tree_to_json_str
  json_str_example = tree_to_json_str(parsed_fol_example)
  # now convert to json object
  parsed_json_example = json.loads(json_str_example, strict=False)
  tfl_example = []
  subscript=2
  construct_tfl_plus_from_fol_json(parsed_json_example, tfl_example, subscript)
  tfl_example_str = ''.join(tfl_example)
  tfl_example_str = tfl_example_str.replace("()","")
  return tfl_example_str


def fol_to_clif(fol_string):
  clif_string = ""
  for i in range(len(fol_string)):
    if fol_string[i] == "∀":
      clif_string += "forall "
    elif fol_string[i] == "⊕":
      clif_string += "xor"
    elif fol_string[i] == "→" or fol_string[i] == "↔" or fol_string[i] == "⟷":
      clif_string += "implies"
    elif fol_string[i] == "¬":
      clif_string += "not "
    elif fol_string[i] == "∃":
      clif_string += "exists "
    elif fol_string[i] == "∧":
      clif_string += "and"
    elif fol_string[i] == "∨":
      clif_string += "or"
    else:
      clif_string += fol_string[i]
  return clif_string.lower()


def fol_to_cgif(fol_string):
  cgif_string = ""
  cgif_string += "[" # always start a CGIF statement with [
  symbols = [] # list to store quantified symbols to keep track and add proper syntax to them
  for i in range(len(fol_string)):
    if fol_string[i] == "∀":
      cgif_string += "@every *"
      symbols.append(fol_string[i+1])
    elif fol_string[i] == "∧" or fol_string[i] == "→" or fol_string[i] == "∨" or fol_string[i] == "⊕" or fol_string[i] == "↔" or fol_string[i] == "⟷":
      cgif_string += ""
    elif fol_string[i] == "¬":
      cgif_string += "~"
    elif fol_string[i] == "∃":
      cgif_string += "*"
      symbols.append(fol_string[i+1])
    elif fol_string[i] == "(":
      cgif_string += "[("
    elif fol_string[i] == ")":
      cgif_string += ")]"
    elif fol_string[i] == ",":
      cgif_string += " "
    else:
      if (fol_string[i] in symbols and (fol_string[i-1] == "(" or fol_string[i-1] == "∀" or fol_string[i-1] == "∃" or fol_string[i-1] == ",")):
        cgif_string += "?"
        cgif_string += fol_string[i]
      else:
        cgif_string += fol_string[i]
  cgif_string += "]" # always end a CGIF statement with ]
  cgif_string = cgif_string.replace("*?", "*")
  cgif_string = cgif_string.replace("[~", "~[")
  return cgif_string.lower()


def fol_to_clingo(fol_string):
  custom_cgif_string = ""
  symbols = [] # list to store quantified symbols to keep track and add proper syntax to them
  for i in range(len(fol_string)):
    if fol_string[i] == "∀":
      custom_cgif_string += "forall"
      symbols.append(fol_string[i+1])
    elif fol_string[i] == "⊕":
      custom_cgif_string += "^"
    elif fol_string[i] == "→":
      custom_cgif_string += "-:"
    elif fol_string[i] == "¬":
      custom_cgif_string += "not"
    elif fol_string[i] == "∃":
      custom_cgif_string += ""
      symbols.append(fol_string[i+1])
    elif fol_string[i] == "∧":
      custom_cgif_string += ","
    elif fol_string[i] == "∨":
      custom_cgif_string += "|"
    elif (fol_string[i] in symbols and (fol_string[i-1] == "∀" or fol_string[i-1] == "∃" or fol_string[i-1] == ",")):
      custom_cgif_string += ""  # eliminate quantifier symbols (e.g., x in ∀x)
    else:
      custom_cgif_string += fol_string[i]
  return custom_cgif_string.lower()


def fol_to_minifol2(fol_string):
  """
  minifol2 is the same as minifol with the removal of "some" entirely for the "∃" symbol (does not replace it with anything else)
  """
  custom_cgif_string = ""
  for i in range(len(fol_string)):
    if fol_string[i] == "∀":
      custom_cgif_string += "all:"
    elif fol_string[i] == "⊕":
      custom_cgif_string += "^"
    elif fol_string[i] == "→":
      custom_cgif_string += ":-"
    elif fol_string[i] == "¬":
      custom_cgif_string += "~"
    elif fol_string[i] == "∃":
      custom_cgif_string += ""
    elif fol_string[i] == "∧":
      custom_cgif_string += "&"
    elif fol_string[i] == "∨":
      custom_cgif_string += "|"
    else:
      custom_cgif_string += fol_string[i]
  return custom_cgif_string.lower()


def fol_to_minifol3(fol_string):
  """
  minifol3 is the same as minifol with the replacement of the "¬" symbol by "not"
  """
  custom_cgif_string = ""
  for i in range(len(fol_string)):
    if fol_string[i] == "∀":
      custom_cgif_string += "all:"
    elif fol_string[i] == "⊕":
      custom_cgif_string += "^"
    elif fol_string[i] == "→":
      custom_cgif_string += ":-"
    elif fol_string[i] == "¬":
      custom_cgif_string += "not"
    elif fol_string[i] == "∃":
      custom_cgif_string += "some:"
    elif fol_string[i] == "∧":
      custom_cgif_string += "&"
    elif fol_string[i] == "∨":
      custom_cgif_string += "|"
    else:
      custom_cgif_string += fol_string[i]
  return custom_cgif_string.lower()


def fol_to_minifol4(fol_string):
  """
  minifol4 is the same as minifol with the replacement of the "∧" symbol by ","
  """
  custom_cgif_string = ""
  for i in range(len(fol_string)):
    if fol_string[i] == "∀":
      custom_cgif_string += "all:"
    elif fol_string[i] == "⊕":
      custom_cgif_string += "^"
    elif fol_string[i] == "→":
      custom_cgif_string += ":-"
    elif fol_string[i] == "¬":
      custom_cgif_string += "~"
    elif fol_string[i] == "∃":
      custom_cgif_string += "some:"
    elif fol_string[i] == "∧":
      custom_cgif_string += ","
    elif fol_string[i] == "∨":
      custom_cgif_string += "|"
    else:
      custom_cgif_string += fol_string[i]
  return custom_cgif_string.lower()


def fol_to_minifol(fol_string):
  custom_cgif_string = ""
  for i in range(len(fol_string)):
    if fol_string[i] == "∀":
      custom_cgif_string += "all:"
    elif fol_string[i] == "⊕":
      custom_cgif_string += "^"
    elif fol_string[i] == "→":
      custom_cgif_string += ":-"
    elif fol_string[i] == "¬":
      custom_cgif_string += "~"
    elif fol_string[i] == "∃":
      custom_cgif_string += "some:"
    elif fol_string[i] == "∧":
      custom_cgif_string += "&"
    elif fol_string[i] == "∨":
      custom_cgif_string += "|"
    else:
      custom_cgif_string += fol_string[i]
  return custom_cgif_string.lower()


# clean FOL syllogisms from ";" and "∴" characters
def clean_fol_syllogisms(fol_string):
  fol_string = fol_string.replace(" ;", '\n').replace(" ∴", '\n').replace("_", '')
  return fol_string


# apply SEF to categorize syllogisms in the pilot and train datasets
def categorize_syllogism(statements):
  statements = statements.lower()
  list_of_statements = statements.split('\n')
  list_of_statements = list(filter(None, list_of_statements)) # remove empty strings from list
  categorical_keywords = ["all", "any", "some", "no", "few", "most", "none", "several"]  # define universal and existential keywords for categorical syllogisms
  if "∨" in statements or "⊕" in statements:
    return "disjunctive"
  elif len(list_of_statements) > 3:
    return "complex"
  elif any(x in statements for x in categorical_keywords):
    return "categorical"
  else:
    return "hypothetical"


def count_syllogisms(data_dict):
  '''
  Docstring for count_syllogisms
  
  :param data_dict: list
  :return syllogisms: dict with counts of each syllogism type
  '''
  syllogisms = {'hypothetical': 0, 'disjunctive': 0, 'categorical': 0, 'complex': 0}
  for item in data_dict:
    syllogisms[categorize_syllogism(item)] += 1
  return syllogisms

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
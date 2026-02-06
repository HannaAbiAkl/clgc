import json
import sys
import lark
from lark import Lark

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
    elif fol_string[i] == "→":
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


# generate statistics for each sef category
def count_syllogisms(data_dict):
  syllogisms = {'hypothetical': 0, 'disjunctive': 0, 'categorical': 0, 'complex': 0}
  for item in data_dict:
    syllogisms[item['sef']] += 1
  return syllogisms
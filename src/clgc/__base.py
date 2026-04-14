import json
import sys
import lark
from lark import Lark
from py_toon_format import encode
from xml.etree.ElementTree import ParseError

from abc import ABC, abstractmethod

class Notation(ABC):
    __PARSER = None

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    def validate(self):
        pass

    @abstractmethod
    def categorize(self):
        pass

    @abstractmethod
    def clean_notation(self):
        pass

class FOLSyllogism(Notation):
    __FOL_BNF_GRAMMAR = r"""
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
    __TFL_BNF_GRAMMAR = r"""
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
    term: plus+ minus* T n | minus+ plus* T n
    T: LETTER
    n: NUMBER
    newline: /\n/

    %import common.LETTER
    %import common.INT -> NUMBER
    %import common.WS
    %ignore WS
"""

    __TFLPLUS_BNF_GRAMMAR = r"""
    start: program
    program: [stat]+
    stat: proposition newline
    proposition: atomicproposition | complexproposition
    complexproposition: leftparen proposition rightparen | proposition plus proposition | proposition minus proposition
    atomicproposition: leftparen* (plus+ | minus+) term | leftparen* (plus* | minus*) term | term
    leftparen: "("
    rightparen: ")"
    plus: "+"
    minus: "-"
    term: T n | leftparen* T n | leftparen* (plus* | minus*) T n | leftparen* (plus* | minus*) T n rightparen* | leftparen* (plus* | minus*) T n rightparen* (plus* | minus*) | leftparen* (plus* | minus*) T n leftparen* | | leftparen* (plus+ | minus+) T n leftparen* 
    T: LETTER
    n: NUMBER
    newline: /\n/

    %import common.LETTER
    %import common.INT -> NUMBER
    %import common.WS
    %ignore WS
"""

    __CLIF_BNF_GRAMMAR = r"""
    start: program
    program: [stat]+
    stat: proposition newline | keyword* quantifier* symbol* leftparen* (quantifier symbol)* proposition rightparen* newline | keyword* (quantifier symbol)* leftparen* (quantifier symbol)* proposition rightparen* newline
    proposition: atomicproposition | complexproposition
    complexproposition: keyword* proposition keyword leftparen* (quantifier symbol)* proposition rightparen*
    atomicproposition: leftparen* term* leftparen* term* rightparen*
    !term: (LETTER+) (LETTER+|DIGIT+|"=" | "+" | "-" | "," | "≠")* | (DIGIT+) (LETTER+|DIGIT+|"=" | "+" | "-" | "," | "≠")*
    !leftparen: "("
    !rightparen: ")"
    !keyword: "and" | "not" | "implies" | "or" | "xor"
    !quantifier: "exists" | "forall"
    symbol: LETTER
    newline: /\n/

    %import common.LETTER
    %import common.DIGIT
    %import common.INT -> NUMBER
    %import common.ESCAPED_STRING -> STRING
    %import common.WS
    %ignore WS
"""

    __CGIF_BNF_GRAMMAR = r"""
    start: program
    program: [stat]+
    stat: proposition newline | keyword* quantifier* symbol* leftparen* (quantifier symbol)* proposition* rightparen* newline | keyword* (quantifier symbol)* leftparen* (quantifier symbol)* proposition rightparen* newline
    proposition: atomicproposition | complexproposition
    complexproposition: keyword* proposition keyword leftbracket* leftparen* (quantifier symbol)* proposition rightparen* rightbracket*
    atomicproposition: leftbracket* leftparen* term* leftbracket* leftparen* term* rightparen* rightbracket*
    !term: leftbracket* leftparen* quantifier* (LETTER+) (LETTER+|DIGIT+|"=" | "+" | "-" | "," | "≠" | "?")* | (DIGIT+) (LETTER+|DIGIT+|"=" | "+" | "-" | "," | "≠" | "?")* rightparen* rightbracket*
    !leftbracket: "["
    !rightbracket: "]"
    !leftparen: "("
    !rightparen: ")"
    !keyword: "~" | "?"
    !quantifier: "*" | "@every *"
    symbol: LETTER
    newline: /\n/

    %import common.LETTER
    %import common.DIGIT
    %import common.INT -> NUMBER
    %import common.ESCAPED_STRING -> STRING
    %import common.WS
    %ignore WS
"""

    __CLINGO_BNF_GRAMMAR = r"""
    start: program
    program: [stat]+
    stat: proposition newline | keyword* quantifier* symbol* leftparen* (quantifier symbol)* proposition rightparen* newline | keyword* (quantifier symbol)* leftparen* (quantifier symbol)* proposition rightparen* newline
    proposition: atomicproposition | complexproposition
    complexproposition: keyword* proposition keyword leftparen* (quantifier symbol)* proposition rightparen*
    atomicproposition: leftparen* term* leftparen* term* rightparen*
    !term: (LETTER+) (LETTER+|DIGIT+|"=" | "+" | "-" | "," | "≠")* | (DIGIT+) (LETTER+|DIGIT+|"=" | "+" | "-" | "," | "≠")*
    !leftparen: "("
    !rightparen: ")"
    !keyword: "," | "not" | "-:" | "|" | "^"
    !quantifier: "forall"
    symbol: LETTER
    newline: /\n/

    %import common.LETTER
    %import common.DIGIT
    %import common.INT -> NUMBER
    %import common.ESCAPED_STRING -> STRING
    %import common.WS
    %ignore WS
"""

    __MINIFOL2_BNF_GRAMMAR = r"""
    start: program
    program: [stat]+
    stat: proposition newline | keyword* quantifier* symbol* leftparen* (quantifier symbol)* proposition rightparen* newline | keyword* (quantifier symbol)* leftparen* (quantifier symbol)* proposition rightparen* newline
    proposition: atomicproposition | complexproposition
    complexproposition: keyword* proposition keyword leftparen* (quantifier symbol)* proposition rightparen*
    atomicproposition: leftparen* term* leftparen* term* rightparen*
    !term: leftparen* (LETTER+) (LETTER+|DIGIT+|"=" | "+" | "-" | "," | "≠")* | (DIGIT+) (LETTER+|DIGIT+|"=" | "+" | "-" | "," | "≠")* rightparen*
    !leftparen: "("
    !rightparen: ")"
    !keyword: "&" | "~" | ":-" | "|" | "^" | ":"
    !quantifier: "all"
    symbol: LETTER
    newline: /\n/

    %import common.LETTER
    %import common.DIGIT
    %import common.INT -> NUMBER
    %import common.ESCAPED_STRING -> STRING
    %import common.WS
    %ignore WS
"""

# based on: https://cseweb.ucsd.edu/classes/fa09/cse130/misc/prolog/prolog_tutorial.pdf
# and: https://github.com/simonkrenger/ch.bfh.bti7064.w2013.PrologParser/blob/master/doc/prolog-bnf-grammar.txt
    __PROLOG_BNF_GRAMMAR = r"""
    start: program
    program: [stat]+
    stat: clauselist query newline | query newline | clauselist newline
    clauselist: clause | clauselist clause
    clause: predicate dot | predicate implication predicatelist dot
    predicatelist: predicate | predicatelist comma predicate
    predicate: atom | atom leftparen termlist rightparen
    termlist: term | termlist comma term
    term: numeral | atom | variable | structure
    structure: atom leftparen termlist rightparen
    implication: ":-"
    rightparen: ")"
    leftparen: "("
    mark: "?-"
    query: mark predicatelist dot
    atom: smallatom | "'" string "'"
    smallatom: letter | smallatom character
    variable:  letter | variable character
    letter: LETTER | "_"
    numeral: digit | numeral digit
    digit: NUMBER
    character:  letter | digit | special
    special: "+" | "-" | "*" | "/" | "/\/" | "^" | "~" | ":" | "." | "?" | " " | "\#" | "$" | "\&"
    dot: "."
    comma: ","
    string: character | string character
    newline: /\n/

    %import common.LETTER
    %import common.INT -> NUMBER
    %import common.WS
    %ignore WS
"""

    __GRAMMARS = {
        "fol": __FOL_BNF_GRAMMAR,
        "tfl": __TFL_BNF_GRAMMAR,
        "tfl+": __TFLPLUS_BNF_GRAMMAR,
        "clif": __CLIF_BNF_GRAMMAR,
        "cgif": __CGIF_BNF_GRAMMAR,
        "clingo": __CLINGO_BNF_GRAMMAR,
        "minifol2": __MINIFOL2_BNF_GRAMMAR,
        "prolog": __PROLOG_BNF_GRAMMAR
    }

    __PARSER = Lark(__FOL_BNF_GRAMMAR)
    
    __CATEGORICAL_KEYWORDS = ["all", "any", "some", "no", "few", "most", "none", "several"]

    def __init__(self, syllogism: str):
        self.syllogism = syllogism
        self.statements = syllogism.rstrip("\n").split("\n")
        self.premises = self.statements[:-1]
        self.conclusion = self.statements[-1]

    def __str__(self):
        return f"Premises:\n" + "\n".join(self.premises) + f"\nConclusion:\n{self.conclusion}"

    def __repr__(self):
        return f"FOLSyllogism({self.syllogism})"

    def validate(self, grammar=None):
        # Implement validation logic for the syllogism
        if grammar:
            parser = Lark(self.__GRAMMARS[grammar.lower()])
            self.__PARSER = parser
        else:
            parser = Lark(self.__GRAMMARS['fol'])
            self.__PARSER = parser
        try:
            self.__PARSER.parse(self.syllogism)
            print("Valid syllogism")
        except Exception as e:
            raise ParseError(f"Invalid syllogism: {e}") from e

    def categorize(self):
        # Implement categorization logic for the syllogism
        self.statements = self.syllogism.lower()  # convert all statements to lowercase for easier keyword detection  
        list_of_statements = self.statements.split("\n")
        list_of_statements = list(filter(None, list_of_statements))
        if "∨" in self.statements or "⊕" in self.statements:
            return "disjunctive"
        elif len(list_of_statements) > 3:
            return "complex"
        elif any(s in self.statements for s in self.__CATEGORICAL_KEYWORDS):
            return "categorical"
        else:
            return "hypothetical"
        
    def add_statements(self, new_statements: list):
        '''Add new statement to syllogism'''
        list_of_statements = ''.join(new_statements)
        self.syllogism = self.syllogism  + list_of_statements
        self.statements = self.syllogism.rstrip("\n").split("\n")
        self.premises = self.statements[:-1]
        self.conclusion = self.statements[-1]

    def add_premises(self, new_premises):
        '''Add new premises to syllogism'''
        list_of_premises = ''.join(new_premises)
        self.premises = self.premises + list_of_premises.rstrip("\n").split("\n")
        self.statements = list(self.premises) + [self.conclusion]
        self.syllogism = '\n'.join(self.statements)

    def add_conclusion(self, new_conclusion):
        '''Add new conclusion to syllogism'''
        self.premises = self.premises + [self.conclusion]
        self.conclusion = new_conclusion.rstrip("\n")
        self.statements = self.premises + [self.conclusion]
        self.syllogism = '\n'.join(self.statements)
    
    @staticmethod
    def _tree_to_json(item, write, level):
        ''' Helper function for tree_to_json. '''
        indent = '  ' * level
        level += 1
        if isinstance(item, lark.Tree):
            write(f'{indent}{{ "type": "{item.data}", "children": [\n')
            sep = ''
            for child in item.children:
                write(indent)
                write(sep)
                FOLSyllogism._tree_to_json(child, write, level)
                sep = ',\n'
            write(f'{indent}] }}\n')
        elif isinstance(item, lark.Token):
            # reminder: Lark Tokens are directly strings
            # token attrs include: line, end_line, column, end_column, pos_in_stream, end_pos
            write(f'{indent}{{ "type": "{item.type}", "text": "{item}", "line": {item.line}, "col": {item.column} }}\n')
        else:
            assert False, item  # fall-through

    @staticmethod
    def tree_to_json(item, write=None):
        """ Writes a Lark tree as a JSON dictionary. """
        if write is None: write = sys.stdout.write
        FOLSyllogism._tree_to_json(item, write, 0)

    @staticmethod
    def tree_to_json_str(item):
        ''' Returns a Lark tree as a JSON string.'''
        output = []
        FOLSyllogism.tree_to_json(item, output.append)  # will build output in memory
        return ''.join(output)
    
    @staticmethod
    def toonify(json_obj):
        '''Convert json object to toon'''
        return encode(json_obj)

    @classmethod
    def treeify(cls, syllogism_str, grammar=None, format="tree"):
        ''' Returns the tree representation of the syllogism in the specified format (tree, str, json).'''
        if grammar:
            # change parser to match grammar
            parser = Lark(cls.__GRAMMARS[grammar.lower()])
            cls.__PARSER = parser
        else:
            # default to fol grammar
            parser = Lark(cls.__GRAMMARS['fol'])
            cls.__PARSER = parser
            # add closing '\n' to syllogism_str if not already present, since our grammars require it
            if not syllogism_str.endswith("\n"):
                syllogism_str += "\n"
        tree_obj = cls.__PARSER.parse(syllogism_str)
        if format == "str":
            return cls.tree_to_json_str(tree_obj)
        elif format == "json":
            json_str = cls.tree_to_json_str(tree_obj)
            return json.loads(json_str, strict=False)
        else:
            return cls.tree_to_json(tree_obj)

    @classmethod
    def simplify_tree(cls, json_obj):
        """Recursively simplifies the tree structure by removing superfluous information like 'line' and 'col'."""
        for key, value in json_obj.items():
            if isinstance(value, dict):
                if 'line' in value:
                    del value['line']
                if 'col' in value:
                    del value['col']
                cls.simplify_tree(value)
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        if 'line' in item:
                            del item['line']
                        if 'col' in item:
                            del item['col']
                        cls.simplify_tree(item)
            else:
                pass
        return json_obj

    @classmethod
    def convert_to_tfl(cls, json_obj, tfl_list):
        ''' Recursively traverse the JSON object and convert FOL components to TFL components. '''
        for key, value in json_obj.items():
            if isinstance(value, dict):
                cls.convert_to_tfl(value, tfl_list)
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
                            cls.convert_to_tfl(item, tfl_list)
            else:
                pass
    
    @classmethod
    def fol_to_tfl(cls, fol_string):
        '''convert FOL syllogism to TFL syllogism'''
        print("*** FOL STRING:", fol_string)
        parsed_fol_example = cls.__PARSER.parse(fol_string)
        # build JSON string with tree_to_json_str
        json_str_example = FOLSyllogism.tree_to_json_str(parsed_fol_example)
        # now convert to json object
        parsed_json_example = json.loads(json_str_example, strict=False)
        tfl_example = []
        cls.convert_to_tfl(parsed_json_example, tfl_example)
        tfl_example_str = ''.join(tfl_example)
        return tfl_example_str
    
    @classmethod
    def convert_to_tfl_plus(cls, json_obj, tfl_list, subscript):
        ''' Recursively traverse the JSON object and convert FOL components to TFL+ components, while keeping track of subscript for predicates. '''
        for key, value in json_obj.items():
            if isinstance(value, dict):
                cls.convert_to_tfl_plus(value, tfl_list, subscript)
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
                            cls.convert_to_tfl_plus(item, tfl_list, subscript)
            else:
                pass

    @classmethod
    def fol_to_tfl_plus(cls, fol_string):
        '''convert FOL syllogism to TFL+ syllogism'''
        print("*** FOL STRING:", fol_string)
        parsed_fol_example = cls.__PARSER.parse(fol_string)
        # build JSON string with tree_to_json_str
        json_str_example = cls.tree_to_json_str(parsed_fol_example)
        # now convert to json object
        parsed_json_example = json.loads(json_str_example, strict=False)
        tfl_example = []
        subscript=2
        cls.convert_to_tfl_plus(parsed_json_example, tfl_example, subscript)
        tfl_example_str = ''.join(tfl_example)
        tfl_example_str = tfl_example_str.replace("()","")
        return tfl_example_str
    
    @classmethod
    def fol_to_clif(cls, fol_string):
        '''convert FOL syllogism to CLIF syllogism'''
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
    
    @classmethod
    def fol_to_cgif(cls, fol_string):
        '''convert FOL syllogism to CGIF syllogism'''
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
    
    @classmethod
    def fol_to_clingo(cls, fol_string):
        '''convert FOL syllogism to Clingo syllogism'''
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
    
    @classmethod
    def fol_to_minifol2(cls, fol_string):
        '''minifol2 is the same as minifol with the removal of "some" entirely for the "∃" symbol (does not replace it with anything else)'''
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
    
    @classmethod
    def fol_to_minifol3(cls, fol_string):
        '''minifol3 is the same as minifol with the replacement of the "¬" symbol by "not"'''
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
    
    @classmethod
    def fol_to_minifol4(cls, fol_string):
        '''minifol4 is the same as minifol with the replacement of the "∧" symbol by ","'''
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
    
    @classmethod
    def fol_to_minifol(cls, fol_string):
        '''minifol is a custom notation that we created which is the same as FOL but with the replacement of the "∧" symbol by "&" and the replacement of the "∃" symbol by "some:" (instead of eliminating it entirely)'''
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
    
    def clean_notation(self):
        '''Clean FOL syllogisms from ";" and "∴" characters'''
        self.syllogism = self.syllogism.replace(" ;", '\n').replace(" ∴", '\n').replace("_", '')
        return self.syllogism
    
    @classmethod
    def sef_statistics(cls, list_of_syllogisms: list):
        '''Compute statistics on the SEF classes of a list of syllogisms'''
        sef_stats = {"disjunctive": 0, "complex": 0, "categorical": 0, "hypothetical": 0}
        for syllogism in list_of_syllogisms:
            sef_class = syllogism.categorize()
            if sef_class in sef_stats:
                sef_stats[sef_class] += 1
        return sef_stats
from lexer import tokens
import ply.yacc as yacc
from functools import reduce

class Node:
    def __init__(self, name, children):
        self.name = name
        self.children = children
        self.value = None # value for expressiona and strings for rest

    def __str__(self):
        childs = str(reduce(lambda x, y: x + '\n' + y, list(map(str, self.children)), ''))
        return self.name +'\t' + childs.replace('\n', '\n\t')
    def get_name(self):
        return self.name
    
    def get_children(self):
        return self.children
    
    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value

def p_program_data(p):
    'program : DATA program'
    p[0] = Node('program-data', [Node('DATA', [p[1]]), p[2]])

def p_program_construct(p):
    'program : construct program'
    p[0] = Node('program-construct', [p[1], p[2]])
def p_progarm_empty(p):
    'program : '
    p[0] = Node('program-empty', [])
def p_construct_expression(p):
    'construct : expression'
    p[0] = Node('construct-expression', [p[1]])

def p_construct_if(p):
    'construct : IF expression program ENDIF'
    p[0] = Node('construct-if', [p[2], p[3]])

def p_construct_for(p):
    "construct : FOR ID IN expression program ENDFOR"
    p[0] = Node('construct-for', [Node('ID', [p[2]]), p[4], p[5]])

def p_expression_dot(p):
    "expression : expression '.' ID"
    p[0] = Node('expression-dot', [p[1], Node('ID', [p[3]])])

def p_expression_id(p):
    "expression : ID"
    p[0] = Node('expression-id', [Node('ID', [p[1]])])

def p_expression_access(p):
    "expression : expression '[' expression ']'"
    p[0] = Node('expression-access', [p[1], p[3]])

def p_expression_add(p):
    "expression : expression '+' expression"
    p[0] = Node('expression-add', [p[1], p[3]])

def p_expression_sub(p):
    "expression : expression '-' expression"
    p[0] = Node('expression-sub', [p[1], p[3]])

def p_expression_mul(p):
    "expression : expression '*' expression"
    p[0] = Node('expression-mul', [p[1], p[3]])

def p_expression_div(p):
    "expression : expression '/' expression"
    p[0] = Node('expression-div', [p[1], p[3]])

def p_expression_and(p):
    "expression : expression AND expression"
    p[0] = Node('expression-and', [p[1], p[3]])

def p_expression_or(p):
    "expression : expression OR expression"
    p[0] = Node('expression-or', [p[1], p[3]])

def p_expression_not(p):
    "expression : NOT expression"
    p[0] = Node('expression-not', [p[2]])

def p_expression_mod(p):
    "expression : expression '%' expression"
    p[0] = Node('expression-mod', [p[1], p[3]])

def p_expression_number(p):
    "expression : NUMBER"
    p[0] = Node('expression-number', [p[1]])

def p_expression_string(p):
    "expression : STRING"
    p[0] = Node('expression-string', [p[1]])

def p_expression_eq(p):
    "expression : expression EQ expression"
    p[0] = Node('expression-eq', [p[1], p[3]])

def p_expression_neq(p):
    "expression : expression NEQ expression"
    p[0] = Node('expression-neq', [p[1], p[3]])

def p_expression_gt(p):
    "expression : expression GT expression"
    p[0] = Node('expression-gt', [p[1], p[3]])

def p_expression_lt(p):
    "expression : expression LT expression"
    p[0] = Node('expression-lt', [[p[1], p[3]]])

def p_expression_ge(p):
    "expression : expression GE expression"
    p[0] = Node('expression-ge', [[p[1], p[3]]])

def p_expression_le(p):
    "expression : expression LE expression"
    p[0] = Node('expression-lE', [[p[1], p[3]]])

def p_expression_dispatch(p):
    "expression : expression '(' params ')'"
    p[0] = Node('expression-dispatch', [p[1], p[3]])

def p_params_full(p):
    "params : params1"
    p[0] = Node('params-full', [p[1]])

def p_params_empty(p):
    "params : "
    p[0] = Node('params-empty', [])

def p_params1(p):
    "params1 : param ',' params1"
    p[0] = Node('params1', [p[1], p[3]])

def p_params1_1(p):
    "params1 : param"
    p[0] = Node('params1-1', [p[1]])

def p_param(p):
    "param : expression"
    p[0] = Node('param', [p[1]])

s = r"""
Hello, My name is {{ omar }}
my parent name is {{ parent.name.another }}
accessing through square brackets {{ parent.name['another'] }}
I want to condition on something
{{ if count == 1 }}
this is data
{{ omar.parent[name] }}
this is another data
{{ endif }}


and finally this is for loops:
{{ for var in range(1, 5) }}
data inside the loop
{{ var + 1 }}

{{ endfor }}

conditioning on string
{{ if name == "o\"omar'\qmar" }}
yay!
{{ endif }}
"""

precedence = (
    ('left', 'AND', 'OR'),
    ('left', 'EQ', 'NEQ'),
    ('left', 'GT', 'LT', 'LE', 'GE'),
    ('left', '+', '-'),
    ('left', '%', '*', '/'),
    ('left', 'NOT'),
    ('left', '[', '('),
    ('left', '.')
)


parser = yacc.yacc()


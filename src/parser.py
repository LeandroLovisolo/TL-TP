# coding: utf-8

from ply import yacc
from lexer import Lexer
import rule

class Parser:

  tokens = Lexer.tokens

  precedence = (
    ('left',  'PLUS',  'MINUS'),
    ('left',  'TIMES', 'DIVIDE'),
    ('right', 'UPLUS', 'UMINUS'),
    ('left',  'AND'),
    # ('left',  'OR'),
    # ('left',  'POWER'),
    # ('left',  'RGROUP'),
    # ('left',  'ROPT'),
    # ('left',  'COLON'),
    )

  def p_rules(self, t):
    '''rules : rule_definition rules
             | empty'''
    if t[1] is not None:
      self.rules.append(t[1])

  def p_rule_definition(self, t):
    '''rule_definition : RULE       EQUALS element
                       | RULE DOT   EQUALS element
                       | START_RULE EQUALS element'''
    if t[1] == '$':
      t[0] = rule.StartRule(t[3])
    elif t[2] == '.':
      t[0] = rule.FinalRule(t[1], t[4])
    else:
      t[0] = rule.Rule(t[1], t[3])

  def p_element(self, t):
    '''element : primitive
               | rule
               | transform
               | element_and
               | element_or
               | element_power
               | element_group
               | element_optional'''
    t[0] = t[1]

  def p_primitive(self, t):
    '''primitive : BOX
                 | BALL
                 | UNDERSCORE'''
    primitives = {'box'  : rule.Box,
                  'ball' : rule.Ball,
                  '_'    : rule.Underscore}
    t[0] = primitives[t[1]]()

  def p_rule(self, t):
    'rule : RULE'
    t[0] = rule.RuleElement(t[1])

  def p_transform(self, t):
    'transform : element COLON transform_name arith_expr'
    transforms = {'rx' : rule.RX,
                  'ry' : rule.RY,
                  'rz' : rule.RZ,
                  'sx' : rule.SX,
                  'sy' : rule.SY,
                  'sz' : rule.SZ,
                  's'  : rule.S,
                  'tx' : rule.TX,
                  'ty' : rule.TY,
                  'tz' : rule.TZ,
                  'cr' : rule.CR,
                  'cg' : rule.CG,
                  'cb' : rule.CB,
                  'd'  : rule.D}
    element = t[1]
    transform_name = t[3]
    param = t[4]
    t[0] = transforms[transform_name](element, param)

  def p_transform_name(self, t):
    '''transform_name : RX
                      | RY
                      | RZ
                      | SX
                      | SY
                      | SZ
                      | S
                      | TX
                      | TY
                      | TZ
                      | CR
                      | CG
                      | CB
                      | D'''
    t[0] = t[1]

  def p_element_and(self, t):
    'element_and : element AND element'
    t[0] = rule.And(t[1], t[3])

  def p_element_or(self, t):
    'element_or : element OR element'
    t[0] = rule.Or(t[1], t[3])

  def p_element_power(self, t):
    'element_power : element POWER arith_expr'
    t[0] = rule.Power(t[1], t[3])

  def p_element_group(self, t):
    'element_group : LGROUP element RGROUP'
    t[0] = rule.Group(t[2])

  def p_element_optional(self, t):
    'element_optional : LOPT element ROPT'
    t[0] = rule.Optional(t[2])

  def p_arith_expr(self, t):
    '''arith_expr : arith_expr_number
                  | arith_expr_uplus
                  | arith_expr_uminus
                  | arith_expr_parenthesis
                  | arith_expr_plus
                  | arith_expr_minus
                  | arith_expr_times
                  | arith_expr_divide'''
    t[0] = t[1]

  def p_arith_expr_number(self, t):
    'arith_expr_number : NUMBER'
    t[0] = rule.Number(t[1])

  def p_arith_expr_uplus(self, t):
    'arith_expr_uplus : PLUS arith_expr %prec UPLUS'
    t[0] = rule.UPlus(t[2])

  def p_arith_expr_uminus(self, t):
    'arith_expr_uminus : MINUS arith_expr %prec UMINUS'
    t[0] = rule.UMinus(t[2])

  def p_arith_expr_parenthesis(self, t):
    'arith_expr_parenthesis : LPAREN arith_expr RPAREN'
    t[0] = rule.Parenthesis(t[2])

  def p_arith_expr_plus(self, t):
    'arith_expr_plus : arith_expr PLUS arith_expr'
    t[0] = rule.Plus(t[1], t[3])

  def p_arith_expr_minus(self, t):
    'arith_expr_minus : arith_expr MINUS arith_expr'
    t[0] = rule.Minus(t[1], t[3])

  def p_arith_expr_times(self, t):
    'arith_expr_times : arith_expr TIMES arith_expr'
    t[0] = rule.Times(t[1], t[3])

  def p_arith_expr_divide(self, t):
    'arith_expr_divide : arith_expr DIVIDE arith_expr'
    t[0] = rule.Divide(t[1], t[3])

  #############################################################################

  def p_empty(self, t):
    'empty :'

  def p_error(self, t):
    line = self.lexer.find_line(t)
    column = self.lexer.find_column(t)
    print 'Syntax error at line %d, column %d:' % (line, column)
    print self.input.split('\n')[line - 1]
    print ' ' * (column - 1) + '↑'

  def print_node(self, node, l=0):
    import sys
    sys.stdout.write('  ' * l)

    print node
    for i in range(0, len(node)):
      self.print_node(node[i], l+1)
    if isinstance(node, rule.Transform):
      self.print_node(node.param, l+1)

  def __init__(self, input):
    self.rules = []
    self.input = input
    self.lexer = Lexer(input)
    self.parser = yacc.yacc(module=self)
    self.parser.parse(input, lexer=self.lexer.lexer)

    for rule in self.rules:
      self.print_node(rule)

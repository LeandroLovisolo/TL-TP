# coding: utf-8

from ply import yacc
from lexer import Lexer

class Parser:

  tokens = Lexer.tokens

  precedence = (
    ('left',  'PLUS',  'MINUS'),
    ('left',  'TIMES', 'DIVIDE'),
    ('right', 'UPLUS', 'UMINUS'),
    # ('left',  'AND'),
    # ('left',  'OR'),
    # ('left',  'POWER'),
    # ('left',  'RGROUP'),
    # ('left',  'ROPT'),
    # ('left',  'COLON'),
    )

  def p_rules(self, t):
    '''rules : rule_definition rules
             | empty'''

  def p_rule_definition(self, t):
    '''rule_definition : RULE       EQUALS element
                       | RULE DOT   EQUALS element
                       | START_RULE EQUALS element'''
    if t[1] == '$':
      self.rules.append(('START_RULE', t[3]))
    elif t[2] == '.':
      self.rules.append(('FINAL_RULE', t[1], t[4]))
    else:
      self.rules.append(('RULE', t[1], t[3]))

  def p_element(self, t):
    '''element : primitive
               | RULE
               | element transform
               | element AND     element
               | element OR      element
               | element POWER   arith_expr
               | LGROUP  element RGROUP
               | LOPT    element ROPT'''
    if len(t) == 4:
      if t[2] in ['&', '|', '^']:
        t[0] = (t[2], t[1], t[3])
      elif t[1] == '<':
        t[0] = ('OPTIONAL', t[2])
      else:
        t[0] = t[2]
    elif len(t) == 3:
      t[0] = ('TRANSFORM', t[1], t[2])
    else:
      if type(t[1]) == tuple:
        t[0] = t[1] # primitive
      else:
        t[0] = ('USE_RULE', t[1])

  def p_primitive(self, t):
    '''primitive : BOX
                 | BALL
                 | UNDERSCORE'''
    t[0] = ('PRIMITIVE', t[1])

  def p_transform(self, t):
    '''transform : COLON transform_name arith_expr transform
                 | empty'''
    if t[1] is None:
      t[0] = []
    else:
      t[0] = [(t[2], t[3])] + t[4]

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

  def p_arith_expr(self, t):
    '''arith_expr : NUMBER
                  | PLUS       arith_expr            %prec UPLUS
                  | MINUS      arith_expr            %prec UMINUS
                  | LPAREN     arith_expr RPAREN
                  | arith_expr PLUS       arith_expr
                  | arith_expr MINUS      arith_expr
                  | arith_expr TIMES      arith_expr
                  | arith_expr DIVIDE     arith_expr'''

    if len(t) == 2:
      t[0] = ('NUMBER', t[1])
    elif len(t) == 3:
      t[0] = ('UPLUS' if t[1] == '+' else 'UMINUS', t[2])
    else:
      if t[1] == '(':
        t[0] = t[2]
      else:
        t[0] = (t[2], t[1], t[3])

  def p_empty(self, t):
    'empty :'

  def p_error(self, t):
    line = self.lexer.find_line(t)
    column = self.lexer.find_column(t)
    print 'Syntax error at line %d, column %d:' % (line, column)
    print self.input.split('\n')[line - 1]
    print ' ' * (column - 1) + '↑'

  def print_rule(self, rule, l=0):
    import sys
    sys.stdout.write('  ' * l)

    if rule[0] == 'START_RULE':
      print 'START_RULE:'
      self.print_rule(rule[1], l+1)

    elif rule[0] in ['RULE', 'FINAL_RULE']:
      print '%s %s:' % (rule[0], rule[1])
      self.print_rule(rule[2], l+1)

    elif rule[0] in ['PRIMITIVE', 'USE_RULE']:
      print '%s: %s' % (rule[0], rule[1])

    elif rule[0] in ['&', '|', '^']:
      print '%s:' % rule[0]
      self.print_rule(rule[1], l+1)
      self.print_rule(rule[2], l+1)

    elif rule[0] == 'OPTIONAL':
      print 'OPTIONAL:'
      self.print_rule(rule[1], l+1)

    elif rule[0] == 'TRANSFORM':
      print 'TRANSFORM:'
      self.print_rule(rule[1], l+1)
      for transform in rule[2]:
        self.print_rule(transform, l+1)

    elif rule[0] in ['rx', 'ry', 'rz', 'sx', 'sy', 'sz', 's',
                     'tx', 'ty', 'tz', 'cr', 'cg', 'cb', 'd']:
      print '%s:' % rule[0]
      self.print_rule(rule[1], l+1)

    elif rule[0] == 'NUMBER':
      print 'NUMBER: %s' % rule[1]

    elif rule[0] in ['UPLUS', 'UMINUS']:
      print '%s:' % rule[0]
      self.print_rule(rule[1], l+1)

    elif rule[0] in ['+', '-', '*', '/']:
      print '%s:' % rule[0]
      self.print_rule(rule[1], l+1)
      self.print_rule(rule[2], l+1)

    else:
      print '===== UNKNOWN NODE =====:', rule

  def __init__(self, input):
    self.rules = []
    self.input = input
    self.lexer = Lexer(input)
    self.parser = yacc.yacc(module=self)
    self.parser.parse(input, lexer=self.lexer.lexer)

    for rule in self.rules:
      self.print_rule(rule)

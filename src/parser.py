# coding: utf-8

from ply import yacc
from lexer import Lexer

class Parser:

  tokens = Lexer.tokens

  def p_rules(self, t):
    '''rules : rule_definition rules
             | empty'''

  def p_rule_definition(self, t):
    '''rule_definition : RULE       EQUALS element
                       | RULE DOT   EQUALS element
                       | START_RULE EQUALS element'''
    print t, t[1], t[2], t[3]

  def p_element(self, t):
    '''element : primitive
               | RULE
               | element transform
               | element AND     element
               | element OR      element
               | element POWER   arith_expr
               | LGROUP  element RGROUP
               | LOPT    element ROPT'''

  def p_primitive(self, t):
    '''primitive : BOX
                 | BALL
                 | UNDERSCORE'''

  def p_transform(self, t):
    '''transform : COLON transform_name arith_expr transform
                 | empty'''

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

  def p_arith_expr(self, t):
    '''arith_expr : NUMBER
                  | LPAREN     arith_expr RPAREN
                  | PLUS       arith_expr
                  | MINUS      arith_expr
                  | arith_expr PLUS       arith_expr
                  | arith_expr MINUS      arith_expr
                  | arith_expr TIMES      arith_expr
                  | arith_expr DIVIDE     arith_expr'''

  def p_empty(self, t):
    'empty :'

  def p_error(self, t):
    line = self.lexer.find_line(t)
    column = self.lexer.find_column(t)
    print 'Syntax error at line %d, column %d:' % (line, column)
    print self.input.split('\n')[line - 1]
    print ' ' * (column - 1) + '↑'

  def __init__(self, input):
    self.input = input
    self.lexer = Lexer(input)
    self.parser = yacc.yacc(module=self)
    self.parser.parse(input, lexer=self.lexer.lexer)

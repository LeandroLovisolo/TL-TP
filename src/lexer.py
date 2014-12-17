# coding: utf-8

import ply.lex as lex

class Lexer:

  keywords = (
    'BOX', 'BALL',                      # Primitivas
    'RX', 'RY', 'RZ',                   # Rotación
    'SX', 'SY', 'SZ', 'S',              # Escala
    'TX', 'TY', 'TZ',                   # Traslación
    'CR', 'CG', 'CB',                   # Color
    'D'                                 # Máxima profundidad
    )

  tokens = (
    'UNDERSCORE',                       # Primitiva nula
    'COLON',                            # Inicio de una transformación
    'AND', 'OR', 'POWER',               # Operaciones
    'LGROUP', 'RGROUP',                 # Agrupación de operaciones
    'LOPT', 'ROPT',                     # Operación opcional
    'NUMBER',                           # Constantes numéricas
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', # Operaciones aritméticas
    'LPAREN', 'RPAREN',                 # Agrupación de operaciones aritméticas
    'START_RULE', 'RULE', 'EQUALS',     # Reglas
    'DOT',                              # Regla final
    'COMMENT',                          # Comentarios
    'ID'                                # Keywords y nombres de regla
    ) + keywords

  # Keywords y nombres de regla
  def t_ID(self, t):
    r'[a-zA-Z]+'
    if t.value.upper() in Lexer.keywords:
      t.type = t.value.upper()
    else:
      t.type = 'RULE'
    return t

  # Primitivas
  t_UNDERSCORE    = r'_'

  # Inicio de una transformación
  t_COLON         = r':'

  # Operaciones
  t_AND           = r'&'
  t_OR            = r'\|'
  t_POWER         = r'\^'
  t_LGROUP        = r'\['
  t_RGROUP        = r'\]'
  t_LOPT          = r'<'
  t_ROPT          = r'>'

  # Números y aritmética
  t_NUMBER         = r'[0-9]+(\.[0-9]+)?'
  t_PLUS           = r'\+'
  t_MINUS          = r'-'
  t_TIMES          = r'\*'
  t_DIVIDE         = r'/'
  t_LPAREN         = r'\('
  t_RPAREN         = r'\)'

  # Reglas
  t_START_RULE     = r'\$'
  t_DOT            = r'\.'
  t_EQUALS         = r'='

  # Comentarios
  t_ignore_COMMENT = r'\"([^\\\n]|(\\.))*?\"'

  # Caracteres ignorados
  t_ignore     = ' \t\n'

  def t_error(self, t):
    line = self.find_line(t)
    column = self.find_column(t)
    print 'Illegal character at line %d, column %d:' % (line, column)
    print self.input.split('\n')[line - 1]
    print ' ' * (column - 1) + '^'

  # Devuelve el número de línea del token dado
  def find_line(self, t):
    line = 0
    pos = t.lexpos
    while pos != -1:
      line += 1
      pos = self.input.rfind('\n', 0, pos)
    return line

  # Devuelve el número de columna del token dado
  def find_column(self, t):
    last_cr = self.input.rfind('\n', 0, t.lexpos)
    if last_cr < 0: last_cr = 0
    column = (t.lexpos - last_cr) + (1 if last_cr == 0 else 0)
    return column

  def lex(self):
    self.lexer.input(self.input)

  def __init__(self, input):
    self.input = input
    self.lexer = lex.lex(module=self)

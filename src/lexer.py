# coding: utf-8

import ply.lex as lex

class Lexer:
  tokens = (
    'BOX', 'BALL', 'UNDERSCORE',
    'COLON',
    'RX', 'RY', 'RZ',
    'SX', 'SY', 'SZ', 'S',
    'TX', 'TY', 'TZ',
    'CR', 'CG', 'CB',
    'D',
    'AND', 'OR', 'POWER',
    'LGROUP', 'RGROUP',
    'LOPT', 'ROPT',
    'NUMBER',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'LPAREN', 'RPAREN',
    'START_RULE', 'RULE', 'DOT', 'EQUALS',
    'COMMENT'
    )

  # Primitivas
  t_BOX        = r'box'
  t_BALL       = r'ball'
  t_UNDERSCORE = r'_'

  # Inicio de una transformación
  t_COLON      = r':'

  # Rotación
  t_RX         = r'rx'
  t_RY         = r'ry'
  t_RZ         = r'rz'

  # Escala
  t_SX         = r'sx'
  t_SY         = r'sy'
  t_SZ         = r'sz'

  # Traslación
  t_TX         = r'tx'
  t_TY         = r'ty'
  t_TZ         = r'tz'

  # Color
  t_CR         = r'cr'
  t_CG         = r'cg'
  t_CB         = r'cb'

  # Máxima profundidad
  t_D          = r'd'

  # Operaciones
  t_AND        = r'&'
  t_OR         = r'\|'
  t_POWER      = r'\^'
  t_LGROUP     = r'\['
  t_RGROUP     = r'\]'
  t_LOPT       = r'<'
  t_ROPT       = r'>'

  # Números y aritmética
  t_NUMBER     = r'[0-9]+(\.[0-9]+)?'
  t_PLUS       = r'\+'
  t_MINUS      = r'-'
  t_TIMES      = r'\*'
  t_DIVIDE     = r'/'
  t_LPAREN     = r'\('
  t_RPAREN     = r'\)'

  # Reglas
  t_START_RULE = r'\$'
  t_RULE       = r'[a-zA-Z]'
  t_DOT        = r'\.'
  t_EQUALS     = r'='

  # Comentarios
  t_COMMENT    = r'\"([^\\\n]|(\\.))*?\"'

  # Caracteres ignorados
  t_ignore     = ' \t'

  # Seguir número de línea para mejorar el reporte de errores
  def t_newline(self, t):
    r'\n+'
    self.lineno += len(t.value)

  def t_error(self, t):
    line = self.lineno
    column = self.find_column(t)
    print 'Illegal character at line %d, column %d:' % (line, column)
    print self.input.split('\n')[line - 1]
    print ' ' * (column - 1) + '↑'

  # Devuelve el número de columna del token dado
  def find_column(self, t):
    last_cr = self.input.rfind('\n', 0, t.lexpos)
    if last_cr < 0: last_cr = 0
    column = (t.lexpos - last_cr) + (1 if last_cr == 0 else 0)
    return column

  def __init__(self, input):
    self.input = input
    self.lexer = lex.lex(module=self)
    self.lineno = 1
    self.lexer.input(input)

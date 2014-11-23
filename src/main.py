#!/usr/bin/env python2

# coding: utf-8

import argparse
import sys
from lexer import Lexer
from ply.lex import LexError

def parse(path):
  f = open(path)
  input = ''.join(f.readlines())
  f.close()

  lexer = Lexer(input)

  try:
    for tok in lexer.lexer:
      print tok
  except LexError:
    sys.exit(-1)

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('path', metavar='FILE', default='/dev/stdin', nargs='?',
                      help='input file (default: read from standard input)')
  args = parser.parse_args()

  parse(args.path)

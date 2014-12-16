#!/usr/bin/env python2

# coding: utf-8

import argparse
import sys
from ply.lex import LexError
from lexer import Lexer
from parser import Parser

def parse(path):
  f = open(path)
  input = ''.join(f.readlines())
  f.close()

  try:
    parser = Parser(input)
  except LexError:
    sys.exit(-1)

  parser.print_nodes()
  parser.scene.do_render()

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('path', metavar='FILE', default='/dev/stdin', nargs='?',
                      help='input file (default: read from standard input)')
  args = parser.parse_args()

  parse(args.path)

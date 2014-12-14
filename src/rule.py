# coding: utf-8

from visual import *

class Node:
  def __init__(self):
    self.children = []

  def __len__(self):
    return len(self.children)

  def __getitem__(self, index):
    return self.children[index]

################################################################################
# Rules                                                                        #
################################################################################

class Rule(Node):
  def __init__(self, name, element):
    Node.__init__(self)
    self.name = name
    self.children.append(element)

  def __str__(self):
    return self.name

class FinalRule(Rule): pass

class StartRule(Rule):
  def __init__(self, element):
    Rule.__init__(self, '$', element)

################################################################################
# Arithmetic expressions                                                       #
################################################################################

class ArithExpr(Node):
  def value(self):
    raise NotImplementedError()

class Number(ArithExpr):
  def __init__(self, value):
    ArithExpr.__init__(self)
    self._value = float(value)

  def value(self):
    return self._value

  def __str__(self):
    return str(self._value)

class UnaryOp(ArithExpr):
  def __init__(self, child):
    ArithExpr.__init__(self)
    self.children.append(child)

class UPlus(UnaryOp):
  def value(self):
    return self.children[0].value()

class UMinus(UnaryOp):
  def value(self):
    return -1 * self.children[0].value()

class BinaryOp(ArithExpr):
  def __init__(self, left, right):
    ArithExpr.__init__(self)
    self.children.append(left)
    self.children.append(right)

class Plus(BinaryOp):
  def value(self):
    return self.children[0].value() + self.children[1].value()

class Minus(BinaryOp):
  def value(self):
    return self.children[0].value() + self.children[1].value()

class Times(BinaryOp):
  def value(self):
    return self.children[0].value() * self.children[1].value()

class Divide(BinaryOp):
  def value(self):
    return self.children[0].value() / self.children[1].value()

class Parenthesis(ArithExpr):
  def __init__(self, child):
    ArithExpr.__init__(self)
    self.children.append(child)

  def value(self):
    return self.children[0].value()

################################################################################
# Elements                                                                     #
################################################################################

class Element(Node): pass

class Box(Element):
  def render(self, frame=None):
    return box(frame=frame)

class Ball(Element):
  def render(self, frame=None):
    return sphere(frame=frame)

class Underscore(Element): pass

class RuleElement(Element):
  def __init__(self, name):
    Element.__init__(self)
    self.name = name

  def __str__(self):
    return self.name

################################################################################
# Transforms                                                                   #
################################################################################

class Transform(Element):
  def __init__(self, child, param):
    Element.__init__(self)
    self.children.append(child)
    self.param = param

class RX(Transform): pass

class RY(Transform): pass

class RZ(Transform): pass

class SX(Transform): pass

class SY(Transform): pass

class SZ(Transform): pass

class S(Transform): pass

class TX(Transform): pass

class TY(Transform): pass

class TZ(Transform): pass

class ColorTransform(Transform):
  def render(self):
    def change_color(obj):
      r, g, b = obj.color
      rt, gt, bt = self.get_color_transform()
      obj.color = (r * rt, g * gt, b * bt)

    obj = self[0].render()
    vmap(change_color, obj)

  def get_color_transform(self):
    raise NotImplementedError()

class CR(ColorTransform):
  def get_color_transform(self):
    return (self.param.value(), 1, 1)

class CG(ColorTransform):
  def get_color_transform(self):
    return (1, self.param.value(), 1)

class CB(ColorTransform):
  def get_color_transform(self):
    return (1, 1, self.param.value())

class D(Transform): pass

################################################################################
# Operations                                                                   #
################################################################################

class And(Element):
  def __init__(self, left, right):
    Element.__init__(self)
    self.children.append(left)
    self.children.append(right)

class Or(Element):
  def __init__(self, left, right):
    Element.__init__(self)
    self.children.append(left)
    self.children.append(right)

class Power(Element):
  def __init__(self, child, power):
    Element.__init__(self)
    self.children.append(child)
    self.power = power

class Group(Element):
  def __init__(self, child):
    Element.__init__(self)
    self.children.append(child)

class Optional(Element):
  def __init__(self, child):
    Element.__init__(self)
    self.children.append(child)

################################################################################
# Helper code                                                                  #
################################################################################

# Map function for Visual Python objects
def vmap(f, obj):
  if isinstance(obj, frame):
    for child_obj in obj.objects:
      vmap(f, child_obj)
  else:
    f(obj)

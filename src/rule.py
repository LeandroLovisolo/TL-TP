# coding: utf-8

import visual


################################################################################
# Scene                                                                        #
################################################################################

class Scene:
  def __init__(self):
    self.rules = []

  def find_rule(self, name):
    for rule in self.rules:
      if rule.name == name:
        return rule
    raise LookupError('Rule %s not found.' % name)

  def render(self):
    self.find_rule('$').render()

################################################################################
# Node                                                                         #
################################################################################

class Node:
  def __init__(self, scene):
    self.scene = scene
    self.children = []

  def __len__(self):
    return len(self.children)

  def __getitem__(self, index):
    return self.children[index]

  def render(self):
    raise NotImplementedError()

################################################################################
# Rules                                                                        #
################################################################################

class Rule(Node):
  def __init__(self, scene, name, element):
    Node.__init__(self, scene)
    self.name = name
    self.children.append(element)

  def __str__(self):
    return self.name

  def render(self):
    return self.children[0].render()

class FinalRule(Rule): pass

class StartRule(Rule):
  def __init__(self, scene, element):
    Rule.__init__(self, scene, '$', element)

################################################################################
# Arithmetic expressions                                                       #
################################################################################

class ArithExpr(Node):
  def value(self):
    raise NotImplementedError()

class Number(ArithExpr):
  def __init__(self, scene, value):
    ArithExpr.__init__(self, scene)
    self._value = float(value)

  def value(self):
    return self._value

  def __str__(self):
    return str(self._value)

class UnaryOp(ArithExpr):
  def __init__(self, scene, child):
    ArithExpr.__init__(self, scene)
    self.children.append(child)

class UPlus(UnaryOp):
  def value(self):
    return self.children[0].value()

class UMinus(UnaryOp):
  def value(self):
    return -1 * self.children[0].value()

class BinaryOp(ArithExpr):
  def __init__(self, scene, left, right):
    ArithExpr.__init__(self, scene)
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
  def __init__(self, scene, child):
    ArithExpr.__init__(self, scene)
    self.children.append(child)

  def value(self):
    return self.children[0].value()

################################################################################
# Elements                                                                     #
################################################################################

class Element(Node): pass

class Box(Element):
  def render(self):
    return visual.box()

class Ball(Element):
  def render(self):
    return visual.sphere(radius=0.5)

class Underscore(Element): pass

class RuleElement(Element):
  def __init__(self, scene, name):
    Element.__init__(self, scene)
    self.name = name

  def __str__(self):
    return self.name

  def render(self):
    return self.scene.find_rule(self.name).render()


################################################################################
# Transforms                                                                   #
################################################################################

class Transform(Element):
  def __init__(self, scene, child, param):
    Element.__init__(self, scene)
    self.children.append(child)
    self.param = param

class RotationTransform(Transform):
  def render(self):
    obj = self[0].render()
    obj.rotate(angle=visual.radians(self.param.value()),
               axis=self.get_rotation_axis())
    return obj

  def get_rotation_axis(self):
    raise NotImplementedError()

class RX(RotationTransform):
  def get_rotation_axis(self):
    return (1, 0, 0)

class RY(RotationTransform):
  def get_rotation_axis(self):
    return (0, 1, 0)

class RZ(RotationTransform):
  def get_rotation_axis(self):
    return (0, 0, 1)

class SX(Transform): pass

class SY(Transform): pass

class SZ(Transform): pass

class S(Transform): pass

class TranslationTransform(Transform):
  def render(self):
    obj = self[0].render()
    x, y, z = obj.pos
    xt, yt, zt = self.get_translation_transform()
    obj.pos = (x + xt, y + yt, z + zt)
    return obj

  def get_translation_transform(self):
    raise NotImplementedError()

class TX(TranslationTransform):
  def get_translation_transform(self):
    return (self.param.value(), 0, 0)

class TY(TranslationTransform):
  def get_translation_transform(self):
    return (0, self.param.value(), 0)

class TZ(TranslationTransform):
  def get_translation_transform(self):
    return (0, 0, self.param.value())

class ColorTransform(Transform):
  def render(self):
    def change_color(obj):
      r, g, b = obj.color
      rt, gt, bt = self.get_color_transform()
      obj.color = (r * rt, g * gt, b * bt)

    obj = self[0].render()
    vmap(change_color, obj)
    return obj

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
  def __init__(self, scene, left, right):
    Element.__init__(self, scene)
    self.children.append(left)
    self.children.append(right)

  def render(self):
    f = visual.frame()
    leftobj  = self.children[0].render()
    rightobj = self.children[1].render()
    leftobj.frame  = f
    rightobj.frame = f
    return f

class Or(Element):
  def __init__(self, scene, left, right):
    Element.__init__(self, scene)
    self.children.append(left)
    self.children.append(right)

class Power(Element):
  def __init__(self, scene, child, power):
    Element.__init__(self, scene)
    self.children.append(child)
    self.power = power

class Group(Element):
  def __init__(self, scene, child):
    Element.__init__(self, scene)
    self.children.append(child)

  def render(self):
    return self.children[0].render()

class Optional(Element):
  def __init__(self, scene, child):
    Element.__init__(self, scene)
    self.children.append(child)

################################################################################
# Helper code                                                                  #
################################################################################

# Map function for Visual Python objects
def vmap(f, obj):
  if isinstance(obj, visual.frame):
    for child_obj in obj.objects:
      vmap(f, child_obj)
  else:
    f(obj)

# coding: utf-8

from random import randint
from direct.showbase.ShowBase import ShowBase
from panda3d.core import *

################################################################################
# World                                                                        #
################################################################################

class World(ShowBase):
  def __init__(self):
    ShowBase.__init__(self)

    # Background color
    self.setBackgroundColor(0, 0, 0)

    # Directional light
    dlight = DirectionalLight('dlight')
    dlightnp = self.render.attachNewNode(dlight)
    dlightnp.setZ(100)
    dlightnp.setP(-90)
    self.render.setLight(dlightnp)

    # Ambient light
    ambient = AmbientLight('ambient')
    ambient.setColor(Vec4(0.2, 0.2, 0.2, 1))
    ambientnp = self.render.attachNewNode(ambient)
    self.render.setLight(ambientnp)

    # Camera position
    self.disableMouse()
    self.camera.setY(-20)
    mat = Mat4(self.camera.getMat())
    mat.invertInPlace()
    self.mouseInterfaceNode.setMat(mat)
    self.enableMouse()

################################################################################
# Scene                                                                        #
################################################################################

class Scene:
  def __init__(self):
    # Will be filled by the parser
    self.rules = []

    # Scene-wide maximum recursion depth
    self.maxDepth = 30

    # Current recursion depth
    self.currentDepth = 0

    # Rule => (depth, maxDepth) dictionary for rules with custom depth limits
    self.perRuleDepths = {}

    # Will be initialized by self.do_render()
    self.world = None

  def find_rule(self, name):
    criteria = lambda x : x.name == name
    rule = self.__find_rule_with_criteria__(criteria)
    if rule is None: raise LookupError('Rule %s not found.' % name)
    return rule

  def find_final_rule(self, name):
    criteria = lambda x : x.name == name and isinstance(x, FinalRule)
    rule = self.__find_rule_with_criteria__(criteria)
    return rule

  def __find_rule_with_criteria__(self, criteria):
    matching = filter(criteria, self.rules)
    if len(matching) == 0:
      return None
    else:
      return matching[randint(0, len(matching) - 1)]

  def new_detached_node(self):
    node = self.world.render.attachNewNode('node')
    node.setColor(1, 1, 1, 1)
    node.detachNode()
    return node

  def do_render(self):
    self.world = World()
    parent = self.find_rule('$').render()
    parent.reparentTo(self.world.render)
    self.world.run()

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
    node = loader.loadModel("box")
    def setColor(node):
      node.setColor(1, 1, 1, 1)
    nmap(setColor, node)
    return node

class Ball(Element):
  def render(self):
    node = loader.loadModel("ball")
    def setColor(node):
      node.setColor(1, 1, 1, 1)
    nmap(setColor, node)
    return node

class Underscore(Element):
  def render(self):
    return self.scene.new_detached_node()

class RuleElement(Element):
  def __init__(self, scene, name):
    Element.__init__(self, scene)
    self.name = name

  def __str__(self):
    return self.name

  def render(self):
    # Get per-rule recursion limit and current depth
    if self.name in self.scene.perRuleDepths.keys():
      hasPerRuleDepth = True
      currentPerRuleDepth, maxPerRuleDepth = self.scene.perRuleDepths[self.name]
    else:
      hasPerRuleDepth = False

    # Check if recursion limit has been reached
    if self.scene.currentDepth < self.scene.maxDepth and \
       (not hasPerRuleDepth or currentPerRuleDepth < maxPerRuleDepth):

      # Increase recursion depth
      if hasPerRuleDepth:
        currentPerRuleDepth += 1
        self.scene.perRuleDepths[self.name] = (currentPerRuleDepth,
                                               maxPerRuleDepth)
      self.scene.currentDepth += 1

      # Debug information
      # if hasPerRuleDepth:
      #   perRuleStr = "\tRule depth: %d/%d." % (currentPerRuleDepth, maxPerRuleDepth)
      # else: perRuleStr = ""
      # print "Rendering rule %s.\tGlobal depth: %d/%d.%s" \
      #     % (self.name, self.scene.currentDepth, self.scene.maxDepth, perRuleStr)

      # Render final rule if we're at the last recursive call and there is one
      if (self.scene.currentDepth == self.scene.maxDepth or \
          (hasPerRuleDepth and currentPerRuleDepth == maxPerRuleDepth)) and \
         self.scene.find_final_rule(self.name) is not None:
        result = self.scene.find_final_rule(self.name).render()

      # Not the last recursive call or no final rule
      else:
        result = self.scene.find_rule(self.name).render()

      # Decrease recursion depth
      self.scene.currentDepth -= 1
      if hasPerRuleDepth:
        self.scene.perRuleDepths[self.name] = (currentPerRuleDepth,
                                               maxPerRuleDepth)

    # Recursion limit reached
    else:
      result = self.scene.new_detached_node()

    return result

################################################################################
# Transforms                                                                   #
################################################################################

class Transform(Element):
  def __init__(self, scene, child, param):
    Element.__init__(self, scene)
    self.children.append(child)
    self.param = param

class RX(Transform):
  def render(self):
    node = self[0].render()
    node.setP(node.getP() - self.param.value())
    return node

class RY(Transform):
  def render(self):
    node = self[0].render()
    node.setH(node.getH() + self.param.value())
    return node

class RZ(Transform):
  def render(self):
    node = self[0].render()
    node.setR(node.getR() - self.param.value())
    return node

class SX(Transform):
  def render(self):
    node = self[0].render()
    node.setSx(node.getSx() * self.param.value())
    return node

class SY(Transform):
  def render(self):
    node = self[0].render()
    node.setSz(node.getSz() * self.param.value())
    return node

class SZ(Transform):
  def render(self):
    node = self[0].render()
    node.setSy(node.getSy() * self.param.value())
    return node

class S(Transform):
  def render(self):
    node = self[0].render()
    node.setScale(node.getScale() * self.param.value())
    return node

class TX(Transform):
  def render(self):
    parent = self.scene.new_detached_node()
    node = self[0].render()
    node.setX(node.getX() + self.param.value())
    node.reparentTo(parent)
    return parent

class TY(Transform):
  def render(self):
    parent = self.scene.new_detached_node()
    node = self[0].render()
    node.setZ(node.getZ() + self.param.value())
    node.reparentTo(parent)
    return parent

class TZ(Transform):
  def render(self):
    parent = self.scene.new_detached_node()
    node = self[0].render()
    parent.setY(node.getY() + self.param.value())
    node.reparentTo(parent)
    return parent

class ColorTransform(Transform):
  def render(self):
    def change_color(node):
      r, g, b, a = node.getColor()
      rt, gt, bt = self.get_color_transform()
      node.setColor(r * rt, g * gt, b * bt, a)

    node = self[0].render()
    nmap(change_color, node)
    return node

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

class D(Transform):
  def render(self):
    child = self[0]
    while isinstance(child, Transform):
      child = child[0]

    if not isinstance(child, RuleElement):
      print "Ignoring maximum depth transform applied to non-rule element."
      return self[0].render()

    rule = child
    if rule.name not in self.scene.perRuleDepths.keys():
      self.scene.perRuleDepths[rule.name] = (0, self.param.value())
      result = self[0].render()
      self.scene.perRuleDepths.pop(rule.name)
    else:
      result = self[0].render()

    return result


################################################################################
# Operations                                                                   #
################################################################################

class And(Element):
  def __init__(self, scene, left, right):
    Element.__init__(self, scene)
    self.children.append(left)
    self.children.append(right)

  def render(self):
    parent = self.scene.new_detached_node()
    left  = self.children[0].render()
    right = self.children[1].render()
    left.reparentTo(parent)
    right.reparentTo(parent)
    return parent

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

  def render(self):
    # Base cases
    if self.power.value() < 1:
      return self.scene.new_detached_node()
    elif self.power.value() == 1:
      return self[0].render()

    # Recursive case: recursively create and render a new ghost Power node with
    # a smaller power, then render the child node
    else:
      # New Power node with smaller power
      new_power = Power(self.scene, self[0],
                        Number(self.scene, self.power.value() - 1))

      # Accumulate a list of transforms until the first element node is reached
      transforms = []
      child = self[0]
      while isinstance(child, Transform):
        transforms.append((child.__class__, child.param))
        child = child[0]

      # Apply transform chain to each conjunction if element node is a group
      if isinstance(child, Group):
        and_node = And(self.scene, new_power, child[0])
        node = self.build_transform_chain(transforms, and_node)

      # Ignore transforms list otherwise
      else:
        node = And(self.scene, new_power, self[0])

      return node.render()

  def build_transform_chain(self, transforms, node):
    while len(transforms) > 0:
      transform_class, param = transforms.pop()
      node = transform_class(self.scene, node, param)
    return node

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

# Map function for Panda3D nodes
def nmap(f, node):
  f(node)
  for child in node.getChildren():
    nmap(f, child)

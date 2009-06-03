from zope.interface import implements
from zope.schema import ASCIILine
from Products.humanator.form.interfaces import IHumanator

class Humanator(ASCIILine):
    implements(IHumanator)

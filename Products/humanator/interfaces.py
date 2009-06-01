from zope import schema
from zope.interface import Interface

from zope.app.container.constraints import contains
from zope.app.container.constraints import containers

from Products.humanator import humanatorMessageFactory as _

# -*- extra stuff goes here -*-

class IHumanatorfolder(Interface):
    """Humanator folder"""


class IHumanatorquestion(Interface):
    """Humanator question"""


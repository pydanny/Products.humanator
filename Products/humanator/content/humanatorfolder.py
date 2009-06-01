"""Definition of the Todo folder content type
"""

from zope.interface import implements, directlyProvides

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from Products.humanator import humanatorMessageFactory as _
from Products.humanator.interfaces import IHumanatorfolder
from Products.humanator.config import PROJECTNAME

HumanatorfolderSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

HumanatorfolderSchema['title'].storage = atapi.AnnotationStorage()
HumanatorfolderSchema['title'].widget.label = 'Name'
HumanatorfolderSchema['description'].storage = atapi.AnnotationStorage()
HumanatorfolderSchema['description'].widget.description = 'A short summary of the humanator folder.'

schemata.finalizeATCTSchema(HumanatorfolderSchema, folderish=True, moveDiscussion=False)

class Humanatorfolder(folder.ATFolder):
    """A folder that contains todo list items"""
    implements(IHumanatorfolder)

    portal_type = "Humanator folder"
    meta_type = "Humanator folder"
    schema = Humanator

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

atapi.registerType(Humanatorfolder, PROJECTNAME)

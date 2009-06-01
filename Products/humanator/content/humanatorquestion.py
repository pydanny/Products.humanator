"""Definition of the Humanator item content type
"""

from zope.interface import implements, directlyProvides

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from Products.humanator import todoMessageFactory as _
from Products.humanator.interfaces import IHumanatorquestion
from Products.humanator.config import PROJECTNAME

HumanatoritemSchema = folder.ATFolderSchema.copy() + atapi.Schema((


    atapi.TextField(
        name='notes',
        storage = atapi.AnnotationStorage(),
        required=False,
        #searchable=1,
        #default='',
        #schemata ='default',
        widget=atapi.RichWidget(
            description=_(u"Notes for this todo item."),
        ),
    ),

))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

HumanatoritemSchema['title'].storage = atapi.AnnotationStorage()
HumanatoritemSchema['title'].widget.label = 'Question'
HumanatoritemSchema['description'].storage = atapi.AnnotationStorage()
HumanatoritemSchema['description'].widget.visible = {'edit': 'hidden', 'view': 'invisible'}

schemata.finalizeATCTSchema(HumanatoritemSchema, moveDiscussion=False)

class Humanatoritem(folder.ATFolder):
    """Description of the Example Type"""
    implements(IHumanatoritem)

    portal_type = "Humanator item"
    meta_type = "Humanator item"
    schema = HumanatoritemSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

atapi.registerType(Humanatoritem, PROJECTNAME)

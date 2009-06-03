"""Definition of the Humanator question content type
"""

from zope.interface import implements, directlyProvides

from Products.Archetypes import atapi
from Products.ATContentTypes.content import document
from Products.ATContentTypes.content import schemata

from Products.humanator import humanatorMessageFactory as _
from Products.humanator.interfaces import IHumanatorquestion
from Products.humanator.config import PROJECTNAME

HumanatorquestionSchema = document.ATDocumentSchema.copy() + atapi.Schema((


    atapi.StringField(
        name='answer',
        storage = atapi.AnnotationStorage(),
        required=True,
        widget=atapi.StringWidget(
            description=_(u"Notes for this todo question."),
        ),
    ),

))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

HumanatorquestionSchema['title'].storage = atapi.AnnotationStorage()
HumanatorquestionSchema['title'].widget.label = 'Question'
HumanatorquestionSchema['description'].storage = atapi.AnnotationStorage()
HumanatorquestionSchema['description'].widget.visible = {'edit': 'hidden', 'view': 'invisible'}

schemata.finalizeATCTSchema(HumanatorquestionSchema, moveDiscussion=False)

class Humanatorquestion(document.ATDocument):
    """Description of the Humanator questionSchema Type"""
    implements(IHumanatorquestion)

    portal_type = "Humanator question"
    meta_type = "Humanator question"
    schema = HumanatorquestionSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

atapi.registerType(Humanatorquestion, PROJECTNAME)

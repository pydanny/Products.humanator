"""Define a browser view for the 'Todo folder' content type. In the FTI 
configured in profiles/default/types/*.xml, this is being set as the default
view of that content type.
"""

from Acquisition import aq_inner

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.app.content.browser.foldercontents import FolderContentsView

class Humanator_folderView(FolderContentsView):
    """Default view of a Todo folder
    """

    __call__ = ViewPageTemplateFile('humanatorquestion.pt')

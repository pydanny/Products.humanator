"""Define a browser view for the 'Todo folder' content type. In the FTI 
configured in profiles/default/types/*.xml, this is being set as the default
view of that content type.
"""

from Acquisition import aq_inner

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.app.content.browser.foldercontents import FolderContentsView

class Humanator_folderView(FolderContentsView):
    """Default view of a Humanator folder
    """

    __call__ = ViewPageTemplateFile('humanatorfolder.pt')


    def folder_listing(self):
        results = ''
        for i in self.context.objectIds():
            obj = self.context.unrestrictedTraverse('/'.join(self.context.getPhysicalPath()) + '/' + i)
            url = obj.absolute_url()
            title = obj.Title()
            answer = obj.getAnswer()           
            wftool = self.context.portal_workflow
            state = wftool.getInfoFor(obj, 'review_state')
            if state == 'published':
                results += ("<li><p><a href='%s'>%s</a></p><p>%s</p></li>" % (url,title, answer))
            else:
                results += ("<li><p><a href='%s'><strike>%s</strike></a></p><p><strike>%s</strike></p></li>" %
                        (url,title, answer))
        return results 

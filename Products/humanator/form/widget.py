from zope.component import getMultiAdapter
from zope.app.form.browser import ASCIIWidget
from zope.app.form.interfaces import ConversionError
from zope.app.form.browser.textwidgets import renderElement
from zope.i18n import MessageFactory

from Acquisition import aq_inner


_ = MessageFactory('Products.humanator')




class HumanatorWidget(ASCIIWidget):
    def __call__(self):
        humanator = getMultiAdapter((aq_inner(self.context.context), self.request), name='humanator')
        kwargs = {'type': self.type,
                  'name': self.name,
                  'id': self.name,
                  'cssClass': self.cssClass,
                  'style': self.style,
                  'size': self.displayWidth,
                  'extra': self.extra}
        if self.displayMaxWidth:
            kwargs['maxlength'] = self.displayMaxWidth # TODO This is untested.

        text = u"""<div class="humanatorQuestion">%(question)s</p>
        %(element)s
        """% {'question':humanator.question(), 'element':renderElement(self.tag, **kwargs)}
        return text
         
    def _toFieldValue(self, input):
        # Verify the user input against the captcha
        humanator = getMultiAdapter((aq_inner(self.context.context), self.request), name='humanator')
        if not humanator.verify(input):
            raise ConversionError(_(u'The code you entered was wrong, please enter the new one.'))
        return super(HumanatorWidget, self)._toFieldValue(input)
import md5

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
            
        question = humanator.question()

        text = u"""<div class="humanatorQuestion"><p>%(question)s</p>
        <input type="hidden" name="question_id" value="%(id)s" />
        <input type="hidden" name="id_check" value="%(id_check)s" />
        %(element)s
        """ % {'question':question.Title(), 
                'element':renderElement(self.tag, **kwargs), 
                'id':question.id, 
                'id_check':md5.new(question.Title()).hexdigest()}
        return text
         
    def _toFieldValue(self, input):
        # Verify the user input against the captcha
        humanator = getMultiAdapter((aq_inner(self.context.context), self.request), name='humanator')
        if not humanator.verify(input):
            raise ConversionError(_(u'The answer you entered was wrong, please enter the new one.'))
        return super(HumanatorWidget, self)._toFieldValue(input)
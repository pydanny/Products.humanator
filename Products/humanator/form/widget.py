from zope.component import getMultiAdapter
from zope.app.form.browser import ASCIIWidget
from zope.app.form.interfaces import ConversionError
from zope.app.form.browser.textwidgets import renderElement
from zope.i18n import MessageFactory

from Acquisition import aq_inner


_ = MessageFactory('Products.humanator')


class HumanatorWidget(ASCIIWidget):
    def __call__(self):
        captcha = getMultiAdapter((aq_inner(self.context.context), self.request), name='humanator')
        kwargs = {'type': self.type,
                  'name': self.name,
                  'id': self.name,
                  'cssClass': self.cssClass,
                  'style': self.style,
                  'size': self.displayWidth,
                  'extra': self.extra}
        if self.displayMaxWidth:
            kwargs['maxlength'] = self.displayMaxWidth # TODO This is untested.

        return u"""<div class="captchaImage">%s</div>
<div class="captchaAudio"><a href="%s" target="_blank">%s</a></div>
%s""" % (captcha.image_tag(),
         captcha.audio_url(),
         _(u"Listen to audio for this captcha"),
         renderElement(self.tag, **kwargs))
         
    def _toFieldValue(self, input):
        # Verify the user input against the captcha
        captcha = getMultiAdapter((aq_inner(self.context.context), self.request), name='captcha')
        if not captcha.verify(input):
            raise ConversionError(_(u'The code you entered was wrong, please enter the new one.'))
        return super(CaptchaWidget, self)._toFieldValue(input)
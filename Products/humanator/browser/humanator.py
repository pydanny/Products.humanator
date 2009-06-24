# question and verifier generation
# TODO: replace ValueErrors with custom errors

from sys import stderr
import md5

import os.path
import random
import re
import sha
import string
import sys
import time


from Acquisition import aq_inner
from App.config import getConfiguration
from interfaces import IHumanatorView
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from zope.interface import implements

CHARS = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'
# note: no 0/o/O and i/I/1 confusion

COOKIE_ID = 'humanatorsessionid'
WORDLENGTH = 7


# Compute a local secret that is semi-unique to a ZEO cluster or standalone
# Zope. This is not rock-solid, but enough to deter spam-bots. Note that this
# assumes Zope clients in a cluster will all have the same <zodb_db *>
# sections. This keeps Captchas from being predictable
_conf = getConfiguration()
SEKRIT = []
for db in _conf.databases:
    SEKRIT.append(repr(db.config.storage.config.__dict__))
SEKRIT = ''.join(SEKRIT)
SEKRIT = re.sub('at 0x[a-f0-9]+>', 'at MEMORYADDRESS>', SEKRIT)

_TEST_TIME = None

class Humanator(BrowserView):
    implements(IHumanatorView)

    _session_id = None
    __name__ = 'humanator'

    def _generate_session(self):
        """Ensure a session id exists"""
        if self._session_id is None:
            id = sha.new(str(random.randrange(sys.maxint))).hexdigest()
            self._session_id = id

            resp = self.request.response
            if COOKIE_ID in resp.cookies:
                # clear the cookie first, clearing out any expiration cookie
                # that may have been set during verification
                del resp.cookies[COOKIE_ID]
            resp.setCookie(COOKIE_ID, id, path='/')

        
    def question(self):
        pc = getToolByName(self.context, 'portal_catalog')
        results = pc(portal_type='Humanator question', review_state='published')
        if results:
            question = random.sample(results,1)[0]
            question = question.getObject()
        else:
            raise ValueError     
            

        return question

    def verify(self, input):

        # fetch the question
        pc = getToolByName(self.context, 'portal_catalog')
        results = pc(portal_type='Humanator question', review_state='published', id = self.request.form['question_id'])
        if results:
            question = results[0].getObject()
        else:
            # replace this value error with something more specific            
            raise ValueError
            
        # Is this a valid response or is there a faked response attempted?   
        if md5.new(question.Title()).hexdigest() != self.request.form['id_check']:
            # replace this value error with something more specific
            raise ValueError

        # now lets see if the input equals the answer
        if input == question.getAnswer():
            return True
            
        
        return False
                
        
        
    def OLD_verify(self, input):
        result = False
        try:
            for word in self._generate_words():
                result = result or input.upper() == word.upper()
            # Delete the session key, we are done with this captcha
            self.request.response.expireCookie(COOKIE_ID, path='/')
        except KeyError:
            pass # No cookie

        return result

    # Binary data subpages


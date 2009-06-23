# Zope Captcha generation
import os.path
import random
import re
import sha
import string
import sys
import time
from sys import stderr

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

    def _generate_words(self):
        """Create words for the current session

        We generate one for the current 5 minutes, plus one for the previous
        5. This way captcha sessions have a livespan of 10 minutes at most.

        """
        session = self.request[COOKIE_ID]
        nowish = _TEST_TIME or int(time.time() / 300)
        seeds = [sha.new(SEKRIT + session + str(nowish)).digest(),
                 sha.new(SEKRIT + session + str(nowish - 5)).digest()]

        words = []
        for seed in seeds:
            word = []
            for i in range(WORDLENGTH):
                index = ord(seed[i]) % len(CHARS)
                word.append(CHARS[index])
            words.append(''.join(word))
        return words
        
    def question(self):

        pc = getToolByName(self.context, 'portal_catalog')
        results = pc(portal_type='Humanator question', review_state='published')
        if results:
            result = random.sample(results,1)[0]
            result = result.getObject()
        else:
            raise ValueError             
        return result.Title()

    def verify(self, input):
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


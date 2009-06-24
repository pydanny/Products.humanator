# question and verifier generation
# TODO: replace ValueErrors with custom errors

from sys import stderr
import md5

import os.path
import random
import sys


from interfaces import IHumanatorView
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from zope.interface import implements



class Humanator(BrowserView):
    implements(IHumanatorView)

    _session_id = None
    __name__ = 'humanator'

        
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



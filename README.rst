Introduction
============
CAPTCHA has a number of disadvantages such as usability and possibly the false sense of security. As white papers documenting the easy cracking of CAPTCHA become more prevalent, the security issues have been growing in concern.

Humanator relies on a different method of determining if the user is human or not. Rather than rely on images (and audio), the humanator widget asks the user questions such as::

  What is six plus 9?

  Type the word 'human' in all capital letters.

  What is the best programming language of all time?

The user provides the correct answer and the form is then validated.

These questions are created by the content editor and are stored as a custom content object simply called HumanatorQuestions. The widget does a randomized portal catalog search against published HumanatorQuestions and serves that to the user.

Products.humanator has no dependencies.

Basic Usage - Creating Questions
================================

Managing questions is simple:

 1. Install Humanator (see below).
 2. Inside a Plone folder create a HumanatorFolder.
 3. Inside a HumanatorFolder add a HumanatorQuestion (including an answer).
 4. Publish the new HumanatorQuestion.

Basic Usage - Adding to a form
================================

Should work following this pattern::

  from zope.interface import Interface
  from zope.schema import TextLine
  from Products.humanator.form import Humanator
  
  class ITestForm(Interface):
      """
      Test form
      """

      name = TextLine(title=_(u'Name'),
                    description=_(u'Your name'),
                    required=True)

      humanator = Humanator(title  = _('Answer the following question'),
                      description = _('Humanity Check'))  

----

Installing Humanator
====================

This package requires Plone 3.x or later.

Installing without buildout
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Install this package in either your system path packages or in the lib/python
directory of your Zope instance. You can do this using either easy_install or
via the setup.py script.

After installing the package it needs to be registered in your Zope instance.
This can be done by putting a Products.humanator-configure.zcml file in the
etc/package-includes directory with this content::

  <include package="Products.humanator" />

or, alternatively, you can add that line to the configure.zcml in a package or
Product that is already registered.

Installing with buildout
~~~~~~~~~~~~~~~~~~~~~~~~

If you are using `buildout`_ to manage your instance installing
Products.humanator is even simpler. You can install Products.humanator by
adding it to the eggs line for your instance::

  [instance]
  eggs = Products.humanator
  zcml = Products.humanator

The last line tells buildout to generate a zcml snippet that tells Zope
to configure Products.humanator.

If another package depends on the Products.humanator egg or includes its zcml
directly you do not need to specify anything in the buildout configuration:
buildout will detect this automatically.

After updating the configuration you need to run the ''bin/buildout'', which
will take care of updating your system.

.. _buildout: http://pypi.python.org/pypi/zc.buildout


# -*- coding: utf-8 -*-

import logging, urllib
from nose.tools import *

from webtest import TestApp
from mock import Mock

from google.appengine.api.mail import InboundEmailMessage
from google.appengine.api import urlfetch

from mailhandler import *

class TestMailHandler:
	def setUp(self):
		pass

	def tearDown(self):
		pass

	def testReceiveBasic(self):
		mail = InboundEmailMessage(
"""From: =?ISO-2022-JP?B?GyRCJUYlOSVIGyhC?= <from@example.com>
To: =?ISO-2022-JP?B?GyRCJUYlOSVIGyhC?= <to@example.com>, to2@example.com, to3@example.com
Subject: New Issue
X-Enigmail-Version: 1.1.1
Content-Type: text/plain; charset=ISO-2022-JP
Content-Transfer-Encoding: 7bit

Test
""")

		urlfetch.fetch = Mock()
		urllib.urlencode = Mock()

		mail_handler = MailHandler()

		mail_handler.request = Mock()
		mail_handler.request = Mock()
		mail_handler.request.url = 'http://localhost/_ah/mail/to%2ba_track%40test.com'

		mail_handler.receive(mail)

		urlfetch.fetch.assert_call_count(1)
		args, keywords = urlfetch.fetch.call_args
		ok_('url' in keywords)

		urllib.urlencode.assert_call_count(1)
		args, keywords = urllib.urlencode.call_args
		assert_equal(args[0]['issue[project]'], 'to')
		assert_equal(args[0]['issue[tracker]'], 'a_track')
	
	def testRequest(self):
		urlfetch.fetch = Mock()
		urllib.urlencode = Mock()

		app = TestApp(webapp.WSGIApplication([MailHandler.mapping()],
                                         debug=True))
		app.post('/_ah/mail/to@test.com',
"""From: =?ISO-2022-JP?B?GyRCJUYlOSVIGyhC?= <from@example.com>
To: =?ISO-2022-JP?B?GyRCJUYlOSVIGyhC?= <to@example.com>, to2@example.com, to3@example.com
Subject: New Issue
X-Enigmail-Version: 1.1.1
Content-Type: text/plain; charset=ISO-2022-JP
Content-Transfer-Encoding: 7bit

Test
""")

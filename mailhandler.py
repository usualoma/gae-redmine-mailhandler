import logging, email, urllib, os, yaml

from google.appengine.api import mail
from google.appengine.api import urlfetch
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler

class MailHandler(InboundMailHandler):
    def receive(self, mail_message):
        yaml_file = os.path.join(os.path.dirname(__file__), 'config.yaml')
        config = yaml.load(open(yaml_file).read().decode('utf8'))

        project = urllib.unquote_plus(self.request.url.partition('/_ah/mail/')[2]).partition('@')[0].decode('utf8')

        tracker = config['tracker']

        if project.find('+') != -1:
            project, tracker = project.split('+')

        try:
            tracker = config['tracker_aliases'][tracker]
        except KeyError:
            None

        url = config['endpoint'].encode('utf8')
        fields = {
            'key': config['key'].encode('utf8'),
            'email': mail_message.original,
            'allow_override': config['allow_override'].encode('utf8'),
            'unknown_user': config['unknown_user'].encode('utf8'),
            'no_permission_check': config['no_permission_check'].encode('utf8'),
            'issue[project]': project.encode('utf8'),
            'issue[tracker]': tracker.encode('utf8'),
        }

        data = urllib.urlencode(fields)
        result = urlfetch.fetch(url=url,
            payload=data,
            method=urlfetch.POST,
            headers={'Content-Type': 'application/x-www-form-urlencoded'})

        if result.status_code == 403:
            logging.info("Request was denied by your Redmine server. " +
                     "Make sure that 'WS for incoming emails' is enabled in application settings and that you provided the correct API key.")
        elif result.status_code == 422:
            logging.info("Request was denied by your Redmine server. " +
                     "Possible reasons: email is sent from an invalid email address or is missing some information.")
        elif result.status_code >= 400 and result.status_code <= 499:
            logging.info("Request was denied by your Redmine server")
        elif result.status_code >= 500 and result.status_code <= 599:
            logging.info("Failed to contact your Redmine server")
        elif result.status_code == 201:
            logging.info("Proccessed successfully")

        logging.info(str(result.status_code))
        logging.info("Received a message from: " + mail_message.sender)


def main():
    application = webapp.WSGIApplication([MailHandler.mapping()],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()

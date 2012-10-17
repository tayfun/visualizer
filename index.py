import webapp2
import json

from models import TextParser


class MainPage(webapp2.RequestHandler):
    def get(self):
        text = self.request.get('text', None)
        if not text:
            self.response.out.write('')  # no input detected.
        else:
            tp = TextParser(text)
            self.response.out.write(json.dumps(tp.fetch_urls()))

    def post(self):
        self.get()


app = webapp2.WSGIApplication(
        [('/visualize.php', MainPage)],  # make sure this is visualise.php
        debug=True)

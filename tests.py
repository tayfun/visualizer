import unittest
import sys
sys.path.append("/home/tayfun/projects/appengine/google_appengine/")

from models import TextParser


"""
You need these while using AppEngine API from shell:
"""

from google.appengine.api import apiproxy_stub_map
from google.appengine.api import urlfetch_stub
apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap()
apiproxy_stub_map.apiproxy.RegisterStub('urlfetch',
    urlfetch_stub.URLFetchServiceStub())


class TestTextParser(unittest.TestCase):
    text = (""
        "Check out this video of Eric Ries "
        "http://www.youtube.com/watch?v=zGXAVw3vF9A from "
        "Stanford University. It's a good start to understand Lean Startup. "
        "Here is a presentation "
        "you need to see as well "
        "http://www.slideshare.net/startuplessonslearned/2012-05-15-"
        "eric-ries-the-lean-startup-pwc-canada ."
        "NYTIme recently covered him too "
        "http://www.nytimes.com/2010/04/25/business/25unboxed.html "
        "Steve")

    default_response = [{'html': '<iframe width="420" height="315" src="http://www.youtube.com/embed/zGXAVw3vF9A" frameborder="0" allowfullscreen></iframe>',
  'icon': u'http://s.ytimg.com/yts/img/favicon-vfldLzJxy.ico',
  'title': u'Evangelizing for the Lean Startup - YouTube',
  'url': 'http://www.youtube.com/watch?v=zGXAVw3vF9A'},
 {'html': "<iframe src=\"http://www.slideshare.net/slideshow/embed_code/13060535\" width=\"427\" height=\"356\" frameborder=\"0\" marginwidth=\"0\" marginheight=\"0\" scrolling=\"no\" style=\"border:1px solid #CCC;border-width:1px 1px 0;margin-bottom:5px\" allowfullscreen> </iframe> <div style=\"margin-bottom:5px\"> <strong> <a href=\"http://www.slideshare.net/startuplessonslearned/2012-05-15-eric-ries-the-lean-startup-pwc-canada\" title=\"2012 05 15 eric ries the lean startup pwc canada\" target=\"_blank\">2012 05 15 eric ries the lean startup pwc canada</a> </strong> from <strong><a href=\"http://www.slideshare.net/startuplessonslearned\" target=\"_blank\">Eric Ries</a></strong> </div>",
  'icon': 'www.slideshare.net/favicon.ico',
  'title': u'2012 05 15 eric ries the lean startup pwc canada',
  'url': 'http://www.slideshare.net/startuplessonslearned/2012-05-15-eric-ries-the-lean-startup-pwc-canada'}]

    def setUp(self):
        self.seq = range(10)

    def test_simple_links(self):
        # make sure the shuffled sequence does not lose any elements
        tp = TextParser(self.text)
        tp.extract_urls()
        self.assertEqual(tp.urls,
            ['http://www.youtube.com/watch?v=zGXAVw3vF9A',
             'http://www.slideshare.net/startuplessonslearned/2012-05-15-'
             'eric-ries-the-lean-startup-pwc-canada',
             'http://www.nytimes.com/2010/04/25/business/25unboxed.html',
            ])

    def test_complex_urls(self):
        # make sure the shuffled sequence does not lose any elements
        text = """
        Check out this video of Eric Ries
        http://bit.ly/abc from
        Stanford University. It's a good start to understand Lean Startup.
        Here is a presentation
        you need to see as well
        bit.ly/abc
        NYTIme recently covered him too
        www.a.long.and.weird.url.com/yep
        Steve
        """
        tp = TextParser(text)
        tp.extract_urls()
        self.assertEqual(tp.urls,
            ['http://bit.ly/abc',
             'bit.ly/abc',
             'www.a.long.and.weird.url.com/yep',
            ])

    def test_embed_codes(self):
        tp = TextParser(self.text)
        self.assertEqual(tp.fetch_urls(), self.default_response)

    def test_shortened_links(self):
        text = (""
        "Check out this video of Eric Ries "
        "http://bit.ly/aVlV11 from "
        "Stanford University. It's a good start to understand Lean Startup. "
        "Here is a presentation "
        "you need to see as well "
        "http://slidesha.re/M2z64S ."
        "NYTIme recently covered him too "
        "http://nyti.ms/aICucz"
        "Steve")
        tp = TextParser(text)
        self.assertEqual(tp.fetch_urls(), self.default_response)


if __name__ == '__main__':
    unittest.main()

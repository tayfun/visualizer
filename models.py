# coding=utf8

import re
import urlparse

from google.appengine.api import urlfetch
from bs4 import BeautifulSoup
from pyjon import jsparser, interpr
from google.appengine.api.urlfetch_errors import DownloadError


class HtmlParser(object):
    YOUTUBE_EMBED_CODE = '<iframe width="420" height="315" src="' \
        'http://www.youtube.com/embed/%(vid)s" frameborder="0" ' \
        'allowfullscreen></iframe>'

    def __init__(self, response, url):
        self.final_url = response.final_url or url
        self.parse_result = urlparse.urlparse(self.final_url)
        self.soup = BeautifulSoup(response.content)
        self.ctx = interpr.PyJS()

    def get_embed_code(self):
        if self.final_url.find("youtube.com/") > 0:
            vid_list = urlparse.parse_qs(
                    self.parse_result.query).get('v', None)
            if not vid_list:
                return
            vid = vid_list[0]
            return self.YOUTUBE_EMBED_CODE % {'vid': vid}
        elif self.final_url.find("slideshare.net/") > 0:
            page_json = self.soup.find(id="page-json")
            if not page_json:
                return
            page_json_text = page_json.get_text()
            page_json_normalized = page_json_text.strip(
                "<!--").strip("//-->")
            page_json_encoded_str = page_json_normalized.encode('utf8')
            parsed_js = jsparser.parse(page_json_encoded_str)
            self.ctx.exec_(parsed_js)
            return self.ctx.context.slideshare_object.\
                    jsplayer.embed_code.decode('unicode-escape')

    def extract_info(self):
        url_info = dict()
        url_info['url'] = self.final_url
        icon_tag = self.soup.find('link', rel='icon')
        if not icon_tag:
            # checkout the other standard.
            icon_tag = self.soup.find('link', rel='shortcut icon')
        # if no explicit favicon declared, use default.
        if not icon_tag:
            url_info['icon'] = self.parse_result.netloc + "/favicon.ico"
        else:
            url_info['icon'] = icon_tag.attrs['href']
        url_info['title'] = self.soup.title.get_text(strip=True)
        url_info['html'] = self.get_embed_code()
        return url_info


class TextParser(object):
    """
    Thanks to John Gruber, aka Daring Fireball for the RegEx below.
    See: http://daringfireball.net/2010/07/improved_regex_for_matching_urls
    """
    url_regex = re.compile(r"""
        \b  # word boundary
        (
          (?:
            https?://               # http or https protocol
            |                       #   or
            www\d{0,3}[.]           # "www.", "www1.", "www2." … "www999."
            |                           #   or
            [a-z0-9.\-]+[.][a-z]{2,4}/  # domain name followed by a slash
          )
          (?:                       # One or more:
            [^\s()<>]+                  # Run of non-space, non-()<>
            |                           #   or
            \(([^\s()<>]+|(\([^\s()<>]+\)))*\)  # balanced parens, up to 2 lvls
          )+
          (?:                       # End with:
            \(([^\s()<>]+|(\([^\s()<>]+\)))*\)  # balanced parens, up to 2 lvls
            |                               #   or
            # not a space or one of these punct chars
            [^\s`!()\[\]{};:'".,<>?«»“”‘’]
          )
        )
        """, re.VERBOSE | re.IGNORECASE)

    def __init__(self, text):
        self.text = text

    def extract_urls(self):
        self.urls = []
        iterator = self.url_regex.finditer(self.text)
        for match in iterator:
            url = match.group()
            if not url.startswith('http://'):
                url = 'http://' + url
            self.urls.append(url)

    def fetch_urls(self):
        self.extract_urls()
        url_info_list = []
        for url in self.urls:
            try:
                response = urlfetch.fetch(url)
            except DownloadError:
                # URL could not be fetched. Could be because of
                # too many redirects etc.
                continue
            if response.status_code != 200:
                # Page wasn't there. Move along.
                continue
            html_parser = HtmlParser(response, url)
            url_info_list.append(html_parser.extract_info())
        return url_info_list

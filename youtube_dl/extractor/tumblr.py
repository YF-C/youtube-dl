from __future__ import unicode_literals

import re

from .common import InfoExtractor
from ..utils import (
    ExtractorError,
)


class TumblrIE(InfoExtractor):
    _VALID_URL = r'http://(?P<blog_name>.*?)\.tumblr\.com/((post)|(video))/(?P<id>\d*)($|/)'
    _TEST = {
        'url': 'http://tatianamaslanydaily.tumblr.com/post/54196191430/orphan-black-dvd-extra-behind-the-scenes',
        'file': '54196191430.mp4',
        'md5': '479bb068e5b16462f5176a6828829767',
        'info_dict': {
            "title": "tatiana maslany news"
        }
    }

    def _real_extract(self, url):
        m_url = re.match(self._VALID_URL, url)
        video_id = m_url.group('id')
        blog = m_url.group('blog_name')

        url = 'http://%s.tumblr.com/post/%s/' % (blog, video_id)
        webpage = self._download_webpage(url, video_id)

        re_video = r'src=\\x22(?P<video_url>http://%s\.tumblr\.com/video_file/%s/(.*?))\\x22 type=\\x22video/(?P<ext>.*?)\\x22' % (blog, video_id)
        video = re.search(re_video, webpage)
        if video is None:
            raise ExtractorError('Unable to extract video')
        video_url = video.group('video_url')
        ext = video.group('ext')

        # retrieve all available thumbnails
        thumb_list = []
        ma = re.search(r'posters.*?\[(?P<thumb>\\x22.*?\\x22)]', webpage)
        if not ma is None:
            for t in ma.group('thumb').replace(r'\\/', '/').split(','):
                t = t.replace(r'\x22','"')
                if (t[0] == '"') and (t[-1] == '"'):
                    thumb_list.append(t[1:-1])

        # The only place where you can get a title, it's not complete,
        # but searching in other places doesn't work for all videos
        video_title = self._html_search_regex(r'<title>(?P<title>.*?)(?: \| Tumblr)?</title>',
            webpage, 'title', flags=re.DOTALL)

        return [{'id': video_id,
                 'url': video_url,
                 'title': video_title,
                 'thumbnails': thumb_list,
                 'ext': ext
                 }]

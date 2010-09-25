"""
FacebookGraphAPI requires access to the page specified by the page_label
argument and a valid access token granted to a Facebook account that has
administrative access to the page.

This class allows you to dynamically query the Facebook Graph API for info
related to a page. API URLs are constructed according to the name of the
method you call, e.g. api.insights() becomes:
https://graph.facebook.com/17890180291/insights?access_token=...

By using a double underscore between words in the method name, you can access
additional information. For example, adding "__page_views" to the method name
in our previous example will result in the following call and url:
Method: api.insights__page_views()
API URL: https://graph.facebook.com/17890180291/insights/page_views?access_token=...

Some API methods support an additional "period" parameter, where period is
defined in seconds but represented in the URL as "day", "week", "month", or
"lifetime". Consult http://developers.facebook.com/docs/reference/fql/insights
for more info on what periods are supported. To use, simply add an additional
"__<period>" to the end of your method name. For example:
Method: api.insights__page_views_external_referrals__week()
API URL: https://graph.facebook.com/17890180291/insights/page_views_external_referrals/week?access_token=...

Usage:
fb_page_label = "TreeHugger"
api = FacebookGraphAPI(fb_page_label)

Insights examples:
For all insights data, use:
api.insights()

For all insights data since September 5th, 2010:
api.insights(since="2010-09-05")

For total fans of the page:
api.insights__page_fans()

For active users of the page:
api.insights__page_active_users()

Since we're querying on pages, we can also access other info, such as the
page's feed, posts, notes, etc. These calls work the same way as Insights...
api.feed()
api.notes()
api.posts(since="2010-09-05",until="2010-09-08")
...and so on.

Consult the Graph API reference for more info:
http://developers.facebook.com/docs/reference/api/
http://developers.facebook.com/docs/reference/fql/insights
http://developers.facebook.com/docs/reference/api/page
"""
import datetime
import json
import time
import urllib
import urllib2

from models import FacebookPage, FacebookAPIAccessToken


class FacebookGraphAPI(object):

    def __init__(self, page_label):
        self.page = FacebookPage.objects.get(label=page_label)
        self.access_token = FacebookAPIAccessToken.objects.latest()
        self.api_url = "https://graph.facebook.com"
        self.last_url = ''

    def __getattr__(self, name):
        if name.startswith('_'):
            raise AttributeError(name)
        else:
            def caller(**params):
                url = self.construct_api_url(name, params)
                return self.api_request(url)
            return caller

    def construct_api_url(self, method_name, params):
        """
        If the 'since' parameter is provided, it cannot be further back
        than 35 days prior to today or the API will return an error.
        To counter this, if 'since' exceeds 35 days, we amend it to a
        35 day period ending yesterday.

        'since' should be a string in %Y-%m-%d format.
        """
        since = params.get('since', None)
        if since:
            since = datetime.date(*time.strptime(since, "%Y-%m-%d")[0:3])
            today = datetime.date.today()
            delta = today - since
            if delta.days > 35:
                diff = datetime.timedelta(days=36)
                params['since'] = today - diff
        api_method = "/".join(method_name.split('__'))
        params['access_token'] = self.access_token.token
        url = "%s/%s/%s?%s" % (self.api_url,
                               self.page.page_id,
                               api_method,
                               urllib.urlencode(params))
        return url

    def api_request(self, url):
        handle = urllib2.urlopen(url)
        self.last_url = handle.geturl()
        return json.load(handle)

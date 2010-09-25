"""
Using the Graph API requires that we perform OAuth authorization and store
the access token for API requests. The Facebook user logging in MUST have
admin access to all Facebook Pages we're interested in, or empty data responses
will be returned by Facebook.

The OAuth flow works as follows:

1. Request access
https://graph.facebook.com/oauth/authorize?client_id=<client_id>&redirect_uri=http://example.com/facebook&scope=read_insights,manage_pages,offline_access

2. Receive code from FB
http://example.com/facebook?code=<code from FB>

3. Exchange code for access_token
https://graph.facebook.com/oauth/access_token?client_id=<client_id>&redirect_uri=http://example.com/facebook&client_secret=<client_secret>&code=<code from FB>

4. Receive access_token as response
access_token=<client_id>|<partial code from FB>|<additional token text>.

Step 1 will require the user to grant access to our application. The
client_id and redirect_uri parameters are specified in the Django
settings file.

Step 2 will redirect the user to the redirect_uri we specify and append a code
parameter to the url. We will use this code in Step 3.

Step 3 requires that we exchange the code returned in Step 2 for an
access_token. The client_id, redirect_uri, and client_secret parameters are
specified in the Django settings file.

Step 4 is when we receive the access token from Facebook, no further redirects
or steps required. The access_token does not require action on the part of the
requestor. The response in step 4 above is edited to show where prior
requests/info appear in the final result. The access_token includes our
client_id, part of the code from Step 2 (the part before the pipe), and another
string, joined by pipes.

Important Note: "offline_access" must be included in the scope parameter for
step 1 above. This gives us, in theory, an infinite session access_token that
shouldn't require us to re-authorize - that is, our access_token shouldn't
expire. Because this is Facebook, I would expect something to go wrong on
occasion, especially given a lack of documentation for just what "long-lived"
means, so I expect re-authorization to be required every now and again.
"""
import urllib
import urllib2
import urlparse

from django.conf import settings
from django.contrib.sites.models import Site
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

from models import FacebookAPIAccessToken


@login_required
def facebook_authorize(request):
    """
    Obtain authorization for Graph API access.

    If code exists in request.GET, then we should be good to move on to
    Step 3 and exchange the code for an access token. Otherwise, send the
    user to Facebook to grant access to our app.
    """
    site = Site.objects.get_current()
    oauth_base_url = "https://graph.facebook.com/oauth"
    access_token = None
    data = {}
    data["client_id"] = settings.FACEBOOK_API_CLIENT_ID
    data["redirect_uri"] = "http://%s%s" % (site.domain,
                                            settings.FACEBOOK_API_REDIRECT_URI)

    code = request.GET.get('code', None)
    if code:
        data["client_secret"] = settings.FACEBOOK_API_CLIENT_SECRET
        data["code"] = code
        token_url = "%s/access_token" % oauth_base_url
        url = "%s?%s" % (token_url,
                         "&".join(["%s=%s" % (k, v) for k, v in data.items()]))
        fb_handle = urllib2.urlopen(url)
        response = urlparse.parse_qs(fb_handle.read())
        access_token = response.get('access_token', None)
        if access_token:
            access_token = access_token[0]
            fb_obj = FacebookAPIAccessToken.objects.get_or_create(\
                token=access_token)
        fb_handle.close()
    else:
        data["scope"] = "read_insights,manage_pages,offline_access"
        auth_url = "%s/authorize" % oauth_base_url
        return HttpResponseRedirect("%s?%s" % (auth_url,
                                               urllib.urlencode(data)))

    return render_to_response("authorize.html",
                              {"token": access_token},
                              context_instance=RequestContext(request))

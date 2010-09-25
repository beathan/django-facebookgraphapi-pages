django-facebookgraphapi-pages
=============================
django-facebookgraphapi-pages is an app geared towards obtaining Insights and Page API access for Facebook pages through the Graph API. It uses OAuth and long-lived offline access tokens to allow programmatic access to the API. Consult views.py for more info on the OAuth flow, and api.py for API usage examples.

API usage requires a FacebookPage object and a valid access token. The API uses the latest FacebookAPIAccessToken obtained for access, but should the latest be invalid, you will need to re-authorize.

While this app is currently geared towards pages, I believe it will be very simple to extend it to other objects.

Required settings in settings.py
================================
::

  FACEBOOK_API_CLIENT_ID = "<your application id>"
  FACEBOOK_API_CLIENT_SECRET = "<your application secret>"
  FACEBOOK_API_REDIRECT_URI = "<your authorization URL>"

The redirect URI should be the site URL of your Facebook app or a subdirectory of it. For example, if your app's site URL is **http\:\/\/<yoursite.com>/facebook/** , then your authorization URL could be **http\:\/\/<yoursite.com>/facebook/authorize/**.

How to install
==============
Copy the app to your project. You'll need to create a Facebook application for this, so make sure you've included the required settings in settings.py, and add the app to INSTALLED_APPS.

Add the app to your project's urls.py, e.g. **"url(r'^facebook/', include('apps.facebookapi.urls'), name='facebook_api')"**. The app's authorization view defaults to "authorize/", so for this example you would visit **http\:\/\/<yoursite.com>/facebook/authorize/** to perform authorization.

Run **"./manage.py syncdb"** to install the FacebookPage and FacebookAPIAccessToken models. See "API Usage" for more info on the models.

Authorizing
===========
Open your browser and visit your authorization URL (in accordance with the defaults, we'll assume your URL is **http\:\/\/<yoursite.com>/facebook/authorize/**). You should see an "Allow/Don't Allow" page on Facebook if you're logged in. After hitting allow, you'll be returned to your authorization URL and presented with the access token. This token will have been saved as an instance of FacebookAPIAccessToken for later API use, so this is just for your personal edification and no further action should be required before beginning API use.

API Usage
=========
Since this app is geared towards Facebook Pages, you'll need to visit the admin site and create a new FacebookPage. The label can be arbitrary, but the page ID should come from Facebook. Once this is saved, you can begin using the API.

In the following example, we assume your page label is "MyPage":

::

  $> ./manage.py shell
  >>> from facebookapi.api import FacebookGraphAPI
  >>> api = FacebookGraphAPI("MyPage")
  >>> api.insights()

You should then see a pile of text containing all insights data for your page.

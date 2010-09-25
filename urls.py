from django.conf.urls.defaults import *
from views import facebook_authorize


urlpatterns = patterns('',
    url(r'^authorize/$',
        facebook_authorize, name='facebook_authorize'),
)

from django.db import models

from managers import FacebookAPIAccessTokenManager


PERIOD_CHOICES = (
    ('d', 'day'),
    ('w', 'week'),
    ('m', 'month'),
    ('l', 'lifetime'),
)


class FacebookAPIAccessToken(models.Model):
    token = models.CharField(max_length=255)
    creation_date = models.DateTimeField(auto_now=True, auto_now_add=True)
    objects = FacebookAPIAccessTokenManager()

    def __unicode__(self):
        return u"%s" % self.token


class FacebookPage(models.Model):
    label = models.CharField(max_length=255)
    page_id = models.CharField(max_length=255)

    def __unicode__(self):
        return u"%s" % self.label

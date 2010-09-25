from django.db import models


class FacebookAPIAccessTokenManager(models.Manager):

    def latest(self):
        return self.order_by('-creation_date')[0]

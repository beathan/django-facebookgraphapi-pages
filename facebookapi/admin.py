from django.contrib import admin

from models import FacebookPage, FacebookAPIAccessToken


class FacebookAPIAccessTokenAdmin(admin.ModelAdmin):
    list_display = ('token', 'creation_date')


class FacebookPageAdmin(admin.ModelAdmin):
    list_display = ('label', 'page_id')


admin.site.register(FacebookAPIAccessToken, FacebookAPIAccessTokenAdmin)
admin.site.register(FacebookPage, FacebookPageAdmin)

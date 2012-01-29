# -*- Mode: python; indent-tabs-mode: nil; c-basic-offset: 2; tab-width: 2 -*-

from django.contrib import admin
from tagging.models import Tag, TaggedItem
from tagging.forms import TagAdminForm
from tagging.views import json_autocomplete

class TagAdmin(admin.ModelAdmin):
  form = TagAdminForm

  def get_urls(self):
      from django.conf.urls.defaults import patterns, url
      urls = super(TagAdmin, self).get_urls()
      my_urls = patterns('',
          url(
              r'autocomplete',
              self.admin_site.admin_view(json_autocomplete),
              name='tagging_autocomplete',
          ),
      )
      return my_urls + urls


admin.site.register(TaggedItem)
admin.site.register(Tag, TagAdmin)





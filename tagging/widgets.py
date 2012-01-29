# -*- Mode: python; indent-tabs-mode: nil; c-basic-offset: 2; tab-width: 2 -*-

from django import forms
from django.utils.safestring import mark_safe
from django.conf import settings
from django.forms.widgets import Input
from django.core.urlresolvers import reverse, NoReverseMatch

class TagAutocomplete(Input):
  input_type = 'text'
  
  def render(self, name, value, attrs=None):
    try:
      list_view = reverse('tagging_autocomplete')
    except NoReverseMatch:
      list_view = reverse('admin:tagging_autocomplete')
    html = super(TagAutocomplete, self).render(name, value, attrs)
    js = u'<script type="text/javascript">$(function() { tagging_autocompleate("%s", "%s"); } );</script>' % (attrs['id'], list_view)
    return mark_safe("\n".join([html, js]))
  
  class Media:
    css = {'all': [ getattr(settings, "TAGGING_JQUERYUI_CSS_URL", "%scss/jquery-ui.css" % settings.STATIC_URL) ] }
    js = (getattr(settings, "TAGGING_JQUERY_URL", "%sjs/jquery.js" % settings.STATIC_URL), 
        getattr(settings, "TAGGING_JQUERYUI_URL", "%sjs/jquery-ui.js" % settings.STATIC_URL), 
        "%stagging/autocomplete.js" % settings.STATIC_URL)



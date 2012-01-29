# -*- Mode: python; indent-tabs-mode: nil; c-basic-offset: 2; tab-width: 2 -*- 
"""
Tagging components for Django's form library.
"""
from django import forms
from django.utils.translation import ugettext as _

from tagging.settings import *
from django.conf import settings
from tagging.models import Tag
from tagging.utils import parse_tag_input
from tagging.widgets import TagAutocomplete

class TagAdminForm(forms.ModelForm):
    class Meta:
        model = Tag

    def clean_name(self):
        value = self.cleaned_data['name']
        tag_names = parse_tag_input(value)
        if len(tag_names) > 1:
            raise forms.ValidationError(_('Multiple tags were given.'))
        elif len(tag_names[0]) > getattr(settings, 'MAX_TAG_LENGTH', MAX_TAG_LENGTH):
            raise forms.ValidationError(
                _('A tag may be no more than %s characters long.') %
                    getattr(settings, 'MAX_TAG_LENGTH', MAX_TAG_LENGTH))
        return value

class TagField(forms.CharField):
    """
    A ``CharField`` which validates that its input is a valid list of
    tag names.
    """
    def clean(self, value):
        value = super(TagField, self).clean(value)
        if value == u'':
            return value
        for tag_name in parse_tag_input(value):
            if len(tag_name) > getattr(settings, 'MAX_TAG_LENGTH', MAX_TAG_LENGTH):
                raise forms.ValidationError(
                    _('Each tag may be no more than %s characters long.') %
                        getattr(settings, 'MAX_TAG_LENGTH', MAX_TAG_LENGTH))
        return value

    def formfield(self, **kwargs):
        defaults = {'widget': TagAutocomplete}
        defaults.update(kwargs)
        if getattr(settings, "TAGGING_AUTOCOMPLETE", TAGGING_AUTOCOMPLETE):
          defaults['widget'] = TagAutocomplete
        return super(TagField, self).formfield(**defaults)


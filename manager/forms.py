#! -*- coding: utf-8 -*-

from django import forms

class VirtualHostForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'input-xlarge',
               'autofocus': 'on'}
    ))
    domain = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'input-xlarge'}
    ))
    description = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'input-xlarge',
               'rows': '3'}), required=False
    )
    is_active = forms.BooleanField(initial=True, required=False)

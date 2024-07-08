from django import forms
from django.forms import ClearableFileInput
from .models import AppMainDocument

class DetailsForm(forms.ModelForm):
    class Meta:
        model = AppMainDocument
        fields = ('docname','doc','doctype','pono')
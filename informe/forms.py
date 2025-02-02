from django import forms
from .models import Link, Banner

class LinkForm(forms.ModelForm):
    class Meta:
        model = Link
        fields = ['title', 'url', 'description']
        

class BannerForm(forms.ModelForm):
    class Meta:
        model = Banner
        fields = ['image', 'link']
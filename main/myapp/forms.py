from dataclasses import fields
from django.forms import ModelForm
from .models import Url

class GetUrl(ModelForm):
    class Meta:
        model = Url
        fields = ['origin_url']
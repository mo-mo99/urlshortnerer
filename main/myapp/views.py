from unittest import result
from django.shortcuts import render
from .forms import GetUrl
import pyshorteners

def index(request):
    if request.method == 'POST':
        form = GetUrl(request.POST, request.FILES)
        if form.is_valid():
            url = form.cleaned_data['text']
            shortner = pyshorteners.Shortener()
            result = shortner.tinyurl.short(url)
        return render(request, 'html/resultpage.html', context={'url': result})

    else:
        form = GetUrl()
        return render(request, 'html/mainpage.html', context={'form': form})
import os
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .forms import GetUrl
import random, string, hashlib
from .models import Url
from django.views.generic import ListView


def index(request):
    if request.method == 'POST':
        form = GetUrl(request.POST, request.FILES)
        if form.is_valid():
            url = form.cleaned_data['origin_url']

            short = get_random_string()
            salt, key = hash_url(short)
            new_url = Url.objects.create(origin_url=url, salt=salt, hash_salted_url=key)
            new_url.save()
            return render(request, 'html/mainpage.html', context={'form': form, 'url': url,
             'key': key, 'short': short})
        
    else:
        form = GetUrl()
        return render(request, 'html/mainpage.html', context={'form': form})


def get_random_string():
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(8))
    return result_str


def hash_url(cur_url):
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac('sha256', cur_url.encode('utf-8'), salt, 100000)
    return salt, key


def check_origin(request, slug):
    salts = Url.objects.values_list('salt', flat=True)
    for index, salt in enumerate(salts):
        new_key = hashlib.pbkdf2_hmac('sha256', slug.encode('utf-8'), salt, 100000)
        key = Url.objects.values_list('hash_salted_url', flat=True)[index]
        if new_key == key:
            return Url.objects.values_list('origin_url')[index]
            break


def check_hashed(request, slug):
    salts = Url.objects.values_list('salt', flat=True)
    for index, salt in enumerate(salts):
        new_key = hashlib.pbkdf2_hmac('sha256', slug.encode('utf-8'), salt, 100000)
        key = Url.objects.values_list('hash_salted_url', flat=True)[index]
        if new_key == key:
            return Url.objects.values_list('hash_salted_url')[index]
            break
            
            
def get_slug(request, **kwargs):
    my_slug = request.resolver_match.kwargs['slug']
    cur_url = Url.objects.get(hash_salted_url=check_hashed(request, my_slug)[0])
    cur_url.visited += 1
    cur_url.save()
    return redirect(check_origin(request, my_slug)[0])
    

def show_links(request):
    links = Url.objects.all().order_by('-visited')
    return render(request, 'html/alllinks.html', context= {'links': links})


def delete_link(request, id):
    
    Url.objects.filter(id=id).delete()
    return HttpResponse('deleted')




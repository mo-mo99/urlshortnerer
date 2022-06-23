import os
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .forms import GetUrl
import random, string, hashlib
from .models import Url
from django.views.generic import ListView

#function for controlling main page that generates the empty form if request method is GET and creates a new Url 
#object in data base if form is valid and submited 

def index(request):
    if request.method == 'POST':
        form = GetUrl(request.POST, request.FILES)
        if form.is_valid():
            url = form.cleaned_data['origin_url']

            if str(url).startswith('http://www.'):   #we need to be sure that origin url has correct format
                short = get_random_string()
                salt, key = hash_url(short)
                new_url = Url.objects.create(origin_url=url, salt=salt, hash_salted_url=key)
                new_url.save()
                return render(request, 'html/mainpage.html', context={'form': form, 'note': short})
            else: 
                note = 'Please write complete link!!!'
                form = GetUrl()
                return render(request, 'html/mainpage.html', context={'form': form, 'note': note})
        
    else:
        form = GetUrl()
        return render(request, 'html/mainpage.html', context={'form': form})


# this function generate for us random string to use as a shortner links

def get_random_string():
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(8))  #the length will be 8
    return result_str


# with the help of Hashlip we can create a hashsalted variable , this function returns salt and hashsalted url
def hash_url(cur_url):
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac('sha256', cur_url.encode('utf-8'), salt, 100000)
    return salt, key


#this function gives us the original url with the help of short url
def check_origin(request, slug):
    salts = Url.objects.values_list('salt', flat=True)
    for index, salt in enumerate(salts):
        new_key = hashlib.pbkdf2_hmac('sha256', slug.encode('utf-8'), salt, 100000)
        key = Url.objects.values_list('hash_salted_url', flat=True)[index]
        if new_key == key:
            return Url.objects.values_list('origin_url')[index][0]
            break


#this function gives us the hashsalted url with the help of short url
def check_hashed(request, slug):
    salts = Url.objects.values_list('salt', flat=True)
    for index, salt in enumerate(salts):
        new_key = hashlib.pbkdf2_hmac('sha256', slug.encode('utf-8'), salt, 100000)
        key = Url.objects.values_list('hash_salted_url', flat=True)[index]
        if new_key == key:
            return Url.objects.values_list('hash_salted_url')[index][0]
            break
            

#this function helps to redirect to original url after getting the slug (short url) from routes            
def get_slug(request, **kwargs):
    my_slug = request.resolver_match.kwargs['slug']
    cur_url = Url.objects.get(hash_salted_url=check_hashed(request, my_slug))
    cur_url.visited += 1   #also we add one visit every time this function get called
    cur_url.save()
    return redirect(check_origin(request, my_slug))
    

#lists all links from database in reverse order
def show_links(request):
    links = Url.objects.all().order_by('-visited')
    return render(request, 'html/alllinks.html', context= {'links': links})


#delete links by id
def delete_link(request, id):
    Url.objects.filter(id=id).delete()
    return redirect('/all-links')




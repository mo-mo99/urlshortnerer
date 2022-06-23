from urllib import response
from django.urls import resolve
from django.test import RequestFactory, TestCase
from requests import request
from .models import Url
from .views import *

class UrlTestCase(TestCase):

    def setUp(self):
        url = 'http://www.google.com'
        short = '12345678'
        salt, key = hash_url(short)
        Url.objects.create(origin_url=url, hash_salted_url=key, salt=salt)
        self.factory = RequestFactory()

    
    def test_model(self):
        cur_url = Url.objects.get(origin_url='http://www.google.com')
        self.assertEqual(cur_url.visited, 0)
        self.assertEqual(type(cur_url.salt), bytes)
        self.assertEqual(type(cur_url.hash_salted_url), bytes)

    
    def test_random_string(self):
        new_str = get_random_string()
        self.assertEquals(len(new_str), 8)
        self.assertEquals(type(new_str), str)
        self.assertTrue(new_str.islower())


    def test_hash_url(self):
        url = 'http://www.google.com'
        salt, key = hash_url(url)
        self.assertEqual(len(salt), 32)
        self.assertEqual(type(salt), bytes)
        self.assertEqual(type(key), bytes)


    def test_check_origin(self):
        cur_url = Url.objects.get(origin_url='http://www.google.com')
        request = self.factory.post('')
        self.assertEqual(check_origin(request, '12345678'), cur_url.origin_url)


    def test_check_hashed(self):
        cur_url = Url.objects.get(origin_url='http://www.google.com')
        request = self.factory.post('')
        self.assertEqual(check_hashed(request, '12345678'), cur_url.hash_salted_url)


    def test_get_slug(self):
        request = self.factory.get('')
        request.resolver_match = resolve('/12345678')
        response = get_slug(request)
        cur_url = Url.objects.get(origin_url='http://www.google.com')
        self.assertEqual(cur_url.visited, 1)
        self.assertEqual(response.status_code, 302)
        

    def test_show_links(self):
        request = self.factory.get('/alllinks')
        response = show_links(request)
        self.assertEqual(response.status_code, 200)
        

    def test_delete_link(self):
        request = self.factory.post('delete')
        cur_url = Url.objects.get(origin_url='http://www.google.com')
        response = delete_link(request, cur_url.id)
        self.assertEqual(len(Url.objects.all()), 0)

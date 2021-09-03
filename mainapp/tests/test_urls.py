from django.test import SimpleTestCase
from django.urls import reverse, resolve
from mainapp.views import BaseView

# для того щоб тести запустились я удалив файл __init__.py з папки mainapp

#TODO: дописати тести


class TestUrls(SimpleTestCase):

    def test_base_url_is_resolved(self):
        url = reverse('base')
        print(resolve(url))
        self.assertEquals(resolve(url).func, BaseView)
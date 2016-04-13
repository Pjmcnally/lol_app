from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from api_query.views import home_page
# from lists.models import Item


class NewVisitorTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html')
        self.assertEqual(response.content.decode(), expected_html)

    def test_home_page_can_save_a_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['summoner_name'] = 'Pjmcnally'

        response = home_page(request)

        self.assertIn('Pjmcnally', response.content.decode())
        self.assertIn('45764164', response.content.decode())

        expected_html = render_to_string(
            'home.html',
            {'sum_name': 'Pjmcnally',
             'sum_id': '45764164'}
        )

        self.assertEqual(expected_html, response.content.decode())

    # def test_home_page_only_saves_items_when_necessary(self):
    #     request = HttpRequest()
    #     home_page(request)
    #     self.assertEqual(Item.objects.count(), 0)


# class ItemModelTest(TestCase):

#     def test_saving_and_retrieving_items(self):
#         sum_name = Item()

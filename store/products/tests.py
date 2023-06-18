from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from products.models import Product


class IndexViewTest(TestCase):

    def test_view(self):
        url = reverse('index')
        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store')
        self.assertTemplateUsed(response, 'products/index.html')


class ProductsListViewTestCase(TestCase):
    fixtures = ['productscategory.json', 'products.json']

    def setUp(self):
        self.products = Product.objects.all()

    def test_list(self):
        url = reverse('products:index')
        response = self.client.get(url)


        self.assertEqual(list(response.context_data['object_list']), list(self.products[:3]))

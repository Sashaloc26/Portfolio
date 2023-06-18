from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from .models import RecipesModel, CategoriesModel


class IndexViewTestCase(TestCase):

    def test_view(self):
        path = reverse('index')
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)


class RecipesViewTestCase(TestCase):

    def setUp(self):
        self.recipes = RecipesModel.objects.all()
        self.categories = CategoriesModel.objects.all()

    fixtures = ['categories2.json', 'recipes2.json']


    def test_list_with_category(self):
        path = reverse('category_recipes', kwargs={'category_id': self.categories.first().id})
        response = self.client.get(path)

        self.assertEqual(response, HTTPStatus.OK)


import random

from django.shortcuts import render
from django.views.generic import ListView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.viewsets import GenericViewSet

from recipes.serializers import UserRecipeRelationSerializer

from .models import CategoriesModel, RecipesModel, UserRecipeRelation


def index(request):
    context = {
        'recipes': RecipesModel.objects.all(),
        'category': CategoriesModel.objects.all(),
    }
    return render(request, 'recipes/index.html', context)


def category_recipes(request, category_id):
    category = CategoriesModel.objects.get(id=category_id)
    recipes = RecipesModel.objects.filter(category=category)
    return render(request, 'recipes/category.html', {'category': category, 'recipes': recipes})


class UserRecipeRelationView(UpdateModelMixin, GenericViewSet):
    queryset = UserRecipeRelation.objects.all()
    serializer_class = UserRecipeRelationSerializer
    lookup_field = 'recipe'

    def get_object(self):
        obj, created = UserRecipeRelation.objects.get_or_create(user=self.request.user,
                                                                recipe_id=self.kwargs['book'])

        return obj


class SearchView(ListView):
    model = RecipesModel
    template_name = 'recipes/search_results.html'
    context_object_name = 'recipes_search'

    def get_queryset(self):
        return RecipesModel.objects.filter(products__icontains=self.request.GET.get('q'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q')
        return context


class RandomRecipeView(ListView):
    model = RecipesModel
    template_name = 'recipes/random_results.html'
    context_object_name = 'random'

    def get_queryset(self):
        return random.choice(RecipesModel.objects.all())

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q')
        return context

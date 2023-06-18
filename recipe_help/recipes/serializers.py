from rest_framework.serializers import ModelSerializer

from .models import CategoriesModel, RecipesModel, UserRecipeRelation


class SerializersRecipe(ModelSerializer):
    class Meta:
        model = RecipesModel
        fields = ('name', 'description', 'products')


class SerializersCategories(ModelSerializer):
    class Meta:
        model = CategoriesModel
        fields = '__all__'


class UserRecipeRelationSerializer(ModelSerializer):
    class Meta:
        model = UserRecipeRelation
        fields = ('recipe', 'like', 'rate')

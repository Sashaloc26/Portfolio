from django.contrib.auth.models import User
from django.db import models


class RecipesModel(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    products = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='media', null=True, blank=True)
    link_video = models.URLField(max_length=255, null=True, blank=True)
    category = models.ForeignKey('CategoriesModel', on_delete=models.CASCADE)
    readers = models.ManyToManyField(User, through='UserRecipeRelation',
                                     related_name='recipes')

    class Meta:
        verbose_name_plural = 'recipes'
        verbose_name = 'recipe'

    def __str__(self):
        return f'Название: {self.name[:20]} | Категория:{self.category.name}'


class CategoriesModel(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return f'{self.name},{self.id}'


class UserRecipeRelation(models.Model):
    RATE_CHOICES = (
        (1, 'Bad'),
        (2, 'Not Bad'),
        (3, 'Good'),
        (4, 'Amazing'),
        (5, 'Incredible')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(RecipesModel, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    rate = models.PositiveSmallIntegerField(choices=RATE_CHOICES, null=True)

    def __str__(self):
        return f' {self.user.username}: {self.recipe.name}, RATE {self.rate}'

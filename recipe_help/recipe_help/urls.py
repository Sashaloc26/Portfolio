"""
URL configuration for recipe_help project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.decorators.cache import cache_page
from rest_framework import routers

from recipes.views import (RandomRecipeView, SearchView,
                           UserRecipeRelationView, category_recipes, index)

app_name = 'recipes'

router = routers.SimpleRouter()
router.register(r'relation', UserRecipeRelationView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', cache_page(30)(index), name='index'),
    path('category/<int:category_id>/', category_recipes, name='category_recipes'),
    path('search/', SearchView.as_view(), name='search'),
    path('random/', RandomRecipeView.as_view(), name='random_recipe')

]

urlpatterns += router.urls

if settings.DEBUG:
    urlpatterns.append(path("__debug__/", include("debug_toolbar.urls")))
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

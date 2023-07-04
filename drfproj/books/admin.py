from django.contrib import admin

from .models import BookRelation, Books


@admin.register(Books)
class BooksAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'genre', 'publish_date')


@admin.register(BookRelation)
class BooksRelationAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'like', 'read', 'rate')

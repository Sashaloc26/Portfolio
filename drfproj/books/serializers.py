from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import BookRelation, Books


class BookSerializer(serializers.ModelSerializer):
    annotated_likes = serializers.IntegerField(read_only=True)
    owner_name = serializers.CharField(source='owner.username', default="",
                                       read_only=True)

    class Meta:
        model = Books
        fields = ('id', 'name', 'author', 'genre', 'publish_date', 'owner_name', 'annotated_likes')


class BookRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookRelation
        fields = ('book', 'like', 'read', 'rate',)

from django.db.models import Case, Count, When
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.viewsets import ModelViewSet

from .models import BookRelation, Books
from .serializers import BookRelationSerializer, BookSerializer


class BookViewSet(ModelViewSet):
    serializer_class = BookSerializer
    queryset = Books.objects.all().annotate(
        annotated_likes=Count(Case(When(bookrelation__like=True, then=1)))).select_related('owner').order_by('id')
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, OrderingFilter]
    filterset_fields = ['name', 'author', 'publish_date']
    search_fields = ['name', 'author']
    ordering_fields = ['name', 'author']


class UserBookRelationView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = BookRelation.objects.all()
    serializer_class = BookRelationSerializer
    lookup_field = 'book'

    def get_object(self):
        obj, _ = BookRelation.objects.get_or_create(user=self.request.user,
                                                    book_id=self.kwargs['book'])
        return obj

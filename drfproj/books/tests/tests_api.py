import json

from django.contrib.auth.models import User
from django.db import connection
from django.db.models import Case, Count, When
from django.test.utils import CaptureQueriesContext
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from books.models import BookRelation, Books
from books.serializers import BookSerializer


class ApiTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_user1')
        self.book_1 = Books.objects.create(id=1, name='test_book_1', author='test_author1',
                                           genre='Comedy', publish_date='2010.12.23')
        self.book_2 = Books.objects.create(id=2, name='test_book_12', author='test_author2',
                                           genre='fantastic', publish_date='2012.11.25')
        self.book_3 = Books.objects.create(id=3, name='test_book_3', author='test_author1',
                                           genre='action', publish_date='2011.10.15')

    def test_get(self):
        url = reverse('books-list')
        with CaptureQueriesContext(connection) as queries:
            response = self.client.get(url)
            self.assertEqual(1, len(queries))
        books = Books.objects.all().annotate(
            annotated_likes=Count(Case(When(bookrelation__like=True, then=1))))
        serializer_data = BookSerializer(books, many=True).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer_data, response.data)

    def test_post(self):
        url = reverse('books-list')
        data = {'name': 'Test_book_post',
                'author': 'author_post',
                'genre': 'genre_post',
                'publish_date': 'date_post'}
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.post(url, data=json_data,
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(4, Books.objects.count())

    def test_update(self):
        url = reverse('books-detail', args=(self.book_1.id,))
        data = {'name': self.book_1.name,
                'author': self.book_1.author,
                'genre': 'genre_post_put_test',
                'publish_date': self.book_1.publish_date}
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.put(url, data=json_data,
                                   content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book_1.refresh_from_db()
        self.assertEqual('genre_post_put_test', self.book_1.genre)

    def test_get_search(self):
        url = reverse('books-list')
        books = Books.objects.filter(id__in=[self.book_1.id, self.book_3.id]).annotate(
            annotated_likes=Count(Case(When(bookrelation__like=True, then=1))))
        response = self.client.get(url, data={'search': 'test_author1'})
        serializer_data = BookSerializer(books, many=True).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer_data, response.data)

    def test_get_filtering(self):
        url = reverse('books-list')
        books = Books.objects.filter(id__in=[self.book_1.id, self.book_3.id]).annotate(
            annotated_likes=Count(Case(When(bookrelation__like=True, then=1))))
        response = self.client.get(url, data={'author': 'test_author1'})
        serializer_data = BookSerializer(books, many=True).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer_data, response.data)


class BookRelationTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_user1')
        self.user_2 = User.objects.create(username='test_user2')
        self.book_1 = Books.objects.create(name='test_book_1', author='test_author1',
                                           genre='Comedy', publish_date='2010.12.23')
        self.book_2 = Books.objects.create(name='test_book_12', author='test_author2',
                                           genre='fantastic', publish_date='2012.11.25')

    def test_like_read(self):
        url = reverse('bookrelation-detail', args=(self.book_1.id,))
        data = {
            'like': True
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.patch(url, data=json_data,
                                     content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relation = BookRelation.objects.get(user=self.user,
                                            book=self.book_1)
        self.assertTrue(relation.like)

        data = {
            'read': True
        }
        json_data = json.dumps(data)
        response = self.client.patch(url, data=json_data,
                                     content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relation = BookRelation.objects.get(user=self.user,
                                            book=self.book_1)
        self.assertTrue(relation.read)

    def test_rate(self):
        url = reverse('bookrelation-detail', args=(self.book_1.id,))
        data = {
            'rate': 4
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.patch(url, data=json_data,
                                     content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relation = BookRelation.objects.get(user=self.user,
                                            book=self.book_1)
        self.assertEqual(4, relation.rate)

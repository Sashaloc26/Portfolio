from django.contrib.auth.models import User
from django.db.models import Case, Count, When
from django.test import TestCase

from books.models import BookRelation, Books
from books.serializers import BookSerializer


class BookSerializersTestCase(TestCase):
    def test_OK(self):
        self.user1 = User.objects.create(username='user1')
        self.user2 = User.objects.create(username='user2')
        self.user3 = User.objects.create(username='user3')
        self.book_1 = Books.objects.create(name='test_book_1', author='test_author1',
                                           genre='Comedy', publish_date='2010.12.23', owner=self.user1)
        self.book_2 = Books.objects.create(name='test_book_2', author='test_author2',
                                           genre='fantastic', publish_date='2012.11.25', owner=self.user2)

        BookRelation.objects.create(user=self.user1, book=self.book_1, like=True,
                                    rate=5)
        BookRelation.objects.create(user=self.user2, book=self.book_1, like=True,
                                    rate=5)
        BookRelation.objects.create(user=self.user3, book=self.book_1, like=True,
                                    rate=4)

        BookRelation.objects.create(user=self.user1, book=self.book_2, like=True,
                                    rate=3)
        BookRelation.objects.create(user=self.user2, book=self.book_2, like=True,
                                    rate=5)
        BookRelation.objects.create(user=self.user3, book=self.book_2, like=False)

        books = Books.objects.all().annotate(
            annotated_likes=Count(Case(When(bookrelation__like=True, then=1))))
        data = BookSerializer(books, many=True).data
        expected_data = [
            {
                'id': self.book_1.id,
                'name': 'test_book_1',
                'author': 'test_author1',
                'genre': 'Comedy',
                'publish_date': '2010.12.23',
                'annotated_likes': 3,
                'owner_name': 'user1',
            },
            {
                'id': self.book_2.id,
                'name': 'test_book_2',
                'author': 'test_author2',
                'genre': 'fantastic',
                'publish_date': '2012.11.25',
                'annotated_likes': 2,
                'owner_name': 'user2',
            },
        ]

        self.assertEqual(expected_data, data)

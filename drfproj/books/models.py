from django.contrib.auth.models import User
from django.db import models


class Books(models.Model):
    name = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    genre = models.CharField(max_length=50)
    publish_date = models.CharField(max_length=50)
    owner = models.ForeignKey(to=User, on_delete=models.SET_NULL,
                              null=True)

    def __str__(self):
        return f'Название:{self.name} Автор:{self.author} Жанр:{self.genre}'

    class Meta:
        verbose_name = 'Book'
        verbose_name_plural = 'Books'


class BookRelation(models.Model):
    RATE_CHOICES = (
        (1, 'Bad'),
        (2, 'Not Bad'),
        (3, 'Good'),
        (4, 'Amazing'),
        (5, 'Incredible')
    )

    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    book = models.ForeignKey(to=Books, on_delete=models.CASCADE)
    read = models.BooleanField(default=False)
    like = models.BooleanField(default=False)
    rate = models.PositiveSmallIntegerField(choices=RATE_CHOICES, null=True)

    def __str__(self):
        return f'{self.user.username}, {self.book.name}, {self.rate}, Прочитано:{self.read}'

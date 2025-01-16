from django.db import models
from django.contrib.auth.models import User


def bookpath(instance,filename):
    return f'books/{instance.title}/{filename}'


class Profile(models.Model):
    USER_TYPE=((1,'Employer'),
               (2,'Teacher'))

    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_name=models.CharField(max_length=244)
    profile_registration=models.CharField(max_length=14)
    profile_type=models.IntegerField(choices=USER_TYPE)


    def __str__(self):
        return self.profile_name


class Author(models.Model):
    author_name=models.CharField(max_length=244)


    def __str__(self):
        return self.author_name


class Genre(models.Model):
    genre_name=models.CharField(max_length=100)

class Book(models.Model):
    STATUS_CHOICES=((1,'Disponível'),
                    (2,'Indisponível'))

    book_title=models.CharField(max_length=244)
    book_picture=models.ImageField(upload_to=bookpath)
    book_author=models.ManyToManyField(Author)
    book_publisher=models.CharField(max_length=244)
    book_edition_number=models.IntegerField()
    book_pnld_code=models.IntegerField()
    book_description=models.TextField()
    number_in_stock=models.IntegerField()
    number_available=models.IntegerField()
    book_status=models.IntegerField(choices=STATUS_CHOICES,max_length=1)
    book_genre=models.ManyToManyField(Genre)


    def __str__(self):
        return self.book_title



    

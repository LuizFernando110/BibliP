from django.db import models
from django.contrib.auth.models import User

def bookpath(instance,filename):
    return f'books/{instance.book_title}/{filename}'


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
    def __str__(self):
        return self.genre_name

class Book(models.Model):
    STATUS_CHOICES=((1,'Disponível'),
                    (2,'Indisponível'))

    book_title=models.CharField(max_length=244)
    book_picture=models.ImageField(upload_to=bookpath)
    book_author=models.ManyToManyField(Author)
    book_publisher=models.CharField(max_length=244)
    book_edition_number=models.IntegerField()
    book_pnld_code=models.CharField(max_length=50)
    book_description=models.TextField()
    number_in_stock=models.IntegerField()
    number_available=models.IntegerField()
    book_status=models.IntegerField(choices=STATUS_CHOICES)
    book_genre=models.ManyToManyField(Genre)


    def __str__(self):
        return self.book_title


class Borrow(models.Model):
    BORROW_STATUS=((1,'analise'),
                   (2,'aberto'),
                   (3,'pendente'),
                   (4,'fechado'))
    

    borrow_teacher=models.ForeignKey(Profile,on_delete=models.CASCADE)
    borrow_book=models.ForeignKey(Book,on_delete=models.CASCADE)
    borrow_receipt_date=models.DateField()
    borrow_delivery_date=models.DateField()
    borrow_status=models.IntegerField(choices=BORROW_STATUS)

    def __str__(self):
        return f'{self.borrow_teacher}:{self.borrow_book}'


class BorrowStudent(models.Model):
    BORROW_STUDENT_STATUS=((1,'Em espera'),
                           (2,'Emprestado'),
                           (3,'Devolvido'),
                           (4,'Atrasado'),
                           (5,'Devolvido com atraso')
                           )


    borrow_holder=models.ForeignKey(Borrow,on_delete=models.CASCADE)
    borrow_student=models.ForeignKey('core.Student',on_delete=models.CASCADE)
    borrow_student_receipt_date=models.DateField()
    borrow_student_delivery_date=models.DateField()
    borrow_student_status=models.IntegerField(choices=BORROW_STUDENT_STATUS)

    def __str__(self):
        return f'{self.borrow_student}:{self.borrow_student_status}'

    

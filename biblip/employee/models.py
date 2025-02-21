from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

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
    book_number_pages=models.IntegerField()
    number_in_stock=models.IntegerField()
    number_available=models.IntegerField()
    book_status=models.IntegerField(choices=STATUS_CHOICES)
    book_genre=models.ManyToManyField(Genre)


    def __str__(self):
        return self.book_title
    
    def save(self,*args,**kwargs):
        if self.pk:
            original = Book.objects.get(pk=self.pk)
            difference = self.number_in_stock - original.number_in_stock
            self.number_available += difference
        else:
            self.number_available = self.number_in_stock 

        self.number_available = min(self.number_available, self.number_in_stock)
        super().save(*args,**kwargs)


class Borrow(models.Model):
    BORROW_STATUS=((1,'analise'),
                   (2,'aberto'),
                   (3,'pendente'),
                   (4,'fechado'))
    

    borrow_teacher=models.ForeignKey(Profile,on_delete=models.CASCADE)
    borrow_schoolclass=models.ForeignKey('core.SchoolClass', on_delete=models.CASCADE)
    borrow_book=models.ForeignKey(Book,on_delete=models.CASCADE)
    borrow_book_number=models.IntegerField()
    borrow_receipt_date=models.DateField()
    borrow_delivery_date=models.DateField()
    borrow_status=models.IntegerField(choices=BORROW_STATUS, default=1)

    def __str__(self):
        return f'{self.borrow_teacher}:{self.borrow_book}'

    def clean(self):
        if self.borrow_book.number_available < self.borrow_book_number:
            raise ValidationError("Não há livros suficientes disponíveis para empréstimo.")
        
    
    def save(self,*args,**kwargs):
        self.clean()

        if self.pk is None:
            self.borrow_book.number_available -= self.borrow_book_number
        else:
            original = Borrow.objects.get(pk=self.pk)
            difference = self.borrow_book_number - original.borrow_book_number
            self.borrow_book.number_available += difference

        self.borrow_book.save()
        super().save(*args,**kwargs)
    
    def delete(self,*args,**kwargs):
        self.borrow_book.number_available += self.borrow_book_number
        self.borrow_book.save()
        super().delete(*args,**kwargs)

class BorrowStudent(models.Model):
    BORROW_STUDENT_STATUS=((1,'Em espera'),
                           (2,'Emprestado'),
                           (3,'Devolvido'),
                           (4,'Atrasado'),
                           (5,'Devolvido com atraso')
                           )


    borrow_holder=models.ForeignKey(Borrow,on_delete=models.CASCADE)
    borrow_student=models.ForeignKey('core.Student',on_delete=models.CASCADE)
    borrow_student_receipt_date=models.DateField(blank=True, null=True)
    borrow_student_delivery_date=models.DateField(blank=True,null=True)
    borrow_student_status=models.IntegerField(choices=BORROW_STUDENT_STATUS)

    def __str__(self):
        return f'{self.borrow_student}:{self.borrow_student_status}'

class BookAuthor(models.Model):
    book=models.ForeignKey(Book,on_delete=models.CASCADE)
    author=models.ForeignKey(Author,on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.book}:{self.author}'
    

class BookGenre(models.Model):
    book=models.ForeignKey(Book,on_delete=models.CASCADE)
    genre=models.ForeignKey(Genre,on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.book}:{self.genre}'
from django.contrib import admin
from .models import Author,Book,BorrowStudent,Borrow,Genre,Profile

admin.site.register(Author)
admin.site.register(Book)
admin.site.register(BorrowStudent)
admin.site.register(Borrow)
admin.site.register(Genre)
admin.site.register(Profile)

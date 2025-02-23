from django.contrib import admin
from .models import Author, Book, BorrowStudent, Borrow, Genre, Profile, BookAuthor, BookGenre

admin.site.register(BorrowStudent)
admin.site.register(Borrow)
admin.site.register(Genre)
admin.site.register(Profile)

class BookAuthorInline(admin.TabularInline):
    model = BookAuthor
    extra = 1

class BookGenreInline(admin.TabularInline):
    model = BookGenre
    extra = 1

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    inlines = [BookAuthorInline, BookGenreInline]
    # readonly_fields = ('number_available',)
    exclude = ('book_author', 'book_genre')
    list_display = ('id','book_title','book_publisher','book_edition_number','book_pnld_code','number_available','book_status',)
    search_fields = ('book_pnld_code', 'book_title',)
    ordering = ('book_title',)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'author_name')
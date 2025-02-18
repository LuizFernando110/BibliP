from django import forms
from django.forms import inlineformset_factory
from .models import Book

class BookForm(forms.ModelForm):

    class Meta:
        model = Book
        fields = ('book_title','book_picture','book_publisher','book_edition_number', 'book_pnld_code', 'book_description', 'book_number_pages', 'number_in_stock', 'book_status')
        widgets = {
            'book_picture': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
        }
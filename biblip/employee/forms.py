from django import forms

class bookRegisterForm(forms.Form):
    book_cover = forms.ImageField()
    book_title = forms.CharField(max_length = 100)
    writer = forms.CharField(max_length = 100)
    publisher = forms.CharField(max_length = 100)
    edition = forms.IntegerField()
    number_of_pages = forms.IntegerField()
    pnld_code = forms.CharField(max_length = 100)
    storage_quantity = forms.IntegerField()
    description = forms.CharField(widget=forms.Textarea)
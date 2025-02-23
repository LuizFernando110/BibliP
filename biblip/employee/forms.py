from django import forms
from django.forms.widgets import ClearableFileInput
from django.forms import inlineformset_factory
from .models import Book,Borrow,BorrowStudent
from formset.widgets import DateInput as formset_DateInput
from django.core.exceptions import ValidationError
from datetime import date

class BookForm(forms.ModelForm):

    class Meta:
        model = Book
        fields = ('book_title','book_picture','book_publisher','book_edition_number', 'book_pnld_code', 'book_description', 'book_number_pages', 'number_in_stock', 'book_status')
        widgets = {
            'book_picture': ClearableFileInput(attrs={'accept': 'image/*'}),
        }

class BorrowForm(forms.ModelForm):

    borrow_receipt_date=forms.DateField(widget=formset_DateInput)
    borrow_delivery_date=forms.DateField(widget=formset_DateInput)
    class Meta:
        model=Borrow
        fields='__all__'
        exclude=('borrow_teacher','borrow_book','borrow_status','borrow_book_number')

    def __init__(self, *args,**kwargs):
        #recebendo perfil de kwargs
        profile=kwargs.pop('profile')
        #recebendo  livro de kwargs
        book=kwargs.pop('book')
        super().__init__(*args,**kwargs)
        self.fields['borrow_schoolclass']=forms.ModelChoiceField(queryset=profile.schoolclass_set.all())
        self.instance.borrow_book=book
        self.instance.borrow_teacher=profile
        #como este form cria borrows passamos como valor de status o número 1(analise)
        self.instance.borrow_status=1

        
    def clean(self):
        cleaned_data=super().clean()
        #validando se usuario é professor

        delivery_date=self.cleaned_data.get('borrow_delivery_date')
        receipt_date=self.cleaned_data.get('borrow_receipt_date')
        if receipt_date<date.today():
            raise ValidationError('data de emprestimo não pode ser anterior a hoje')
        
        if delivery_date<receipt_date:
            raise ValidationError('data de devolução não pode ser anterior a data de empréstimo')

        if self.instance.borrow_teacher.profile_type != 2:
            raise ValidationError('usuario não pode pedir emprestimos')
        
        #validando se livro está disponivel
        if self.instance.borrow_book.book_status != 1:
            raise ValidationError('livro indiponivel')
        
        
        book_number=self.cleaned_data.get('borrow_schoolclass').school_class_students.count()
        if  book_number > self.instance.borrow_book.number_available:
            raise ValidationError('livros insuficientes')
        
        self.cleaned_data['borrow_book_number']=book_number
        
        return cleaned_data
    
 
        
    
    def save(self, commit=True):
        students=self.instance.borrow_schoolclass.school_class_students.all()
        instance=self.instance

        self.instance.borrow_book_number=self.cleaned_data.get('borrow_book_number')
        
        if commit:
            if instance.pk is None:
                instance.save()
                for student in students:
                    BorrowStudent.objects.create(borrow_holder=self.instance,borrow_student=student,borrow_student_status=1)
            return instance
            

        return instance
            

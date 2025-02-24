from django import forms
from .models import SchoolClass,Student
from employee.models import Profile
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

import csv
import io

class ProfileRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    profile_registration = forms.CharField(max_length = 14)
    profile_type = forms.ChoiceField(choices=Profile.USER_TYPE, widget=forms.RadioSelect)

    class Meta:
        model = User
        fields = ['first_name', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['profile_registration']
        user.set_password(self.cleaned_data['password'])
        
        if commit:
            user.save()
            Profile.objects.create(
                user=user,
                profile_name = self.cleaned_data['first_name'],
                profile_type = self.cleaned_data['profile_type'], 
                profile_registration = self.cleaned_data['profile_registration']
            )
            
        return user

class LoginForm(forms.Form):
    username = forms.CharField(max_length=14)
    password = forms.CharField(widget=forms.PasswordInput)
    remember_me = forms.BooleanField(required=False , initial=False)

class SchoolClassForm(forms.ModelForm):
    school_class_students_wid=forms.FileField()
      
    def csv_file_clean(self):
        #recebendo o arquivo do input
        temp_file=self.cleaned_data.get('school_class_students_wid')
        lista=[]
        for chunk in temp_file.chunks():
            #usamos decode para transformar o arquivo de bytes para string
            #usamos io.StringIO para transformar a string em um objeto que se comporta como um arquivo e o passamos para o
            #csv.dictreader, cada linha foi transformada em um dicionario com as chaves sendo as colunas
            csv_teste=csv.DictReader(io.StringIO(chunk.decode('utf-8')))
            for i in csv_teste:
                #verificando se o arquivo tem as chaves corretas
                if 'matricula' not in i or 'nome' not in i:
                    raise ValidationError('arquivo de turma não contem a(s) coluna(s) matricula e/ou nome')
                matricula=i.get('matricula')
                nome=i.get('nome')
                #validando se as chaves tem dados corretos
                if nome.strip()=='' or matricula.strip()=='':
                    raise ValidationError('aluno com dados faltando')
                lista.append({'matricula':matricula,'nome':nome})
            self.cleaned_data['school_class_students_dict']=lista

    def csv_file_save(self,relation):

            #lendo dicionario de cleaned data
        for s in self.cleaned_data.get('school_class_students_dict'):
            student=Student.objects.filter(student_registration=s.get('matricula')).first()
            if student:
                relation.append(student)
            else:
                student=Student.objects.create(student_name=s.get('nome'),student_registration=s.get('matricula'))
                relation.append(student)
        return relation

    def clean(self):
        #pegando o valor padrão do clean
        cleaned_data=super().clean()

        self.csv_file_clean()
        
        return cleaned_data 
    

    def save(self,profile,commit=True):
        '''profile=request.user.profile on view'''
        self.instance.school_class_teacher=profile
        instance=super(SchoolClassForm,self).save(commit=False)

        if commit:
            relation=[]
            self.csv_file_save(relation=relation)
            #salvando no db
            instance.save()
            #adicionando as relações
            instance.school_class_students.add(*relation)
        return instance
    
    class Meta:
        model=SchoolClass
        fields=['school_class_name']
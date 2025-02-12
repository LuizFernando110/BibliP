from django import forms 
from .models import SchoolClass,Student
from employee.models import Profile
from django.contrib.auth.models import User
from django.core.files.temp import NamedTemporaryFile
import csv

class loginTeacherForm(forms.ModelForm):
    teacherEnrollment = forms.CharField(max_length = 14,
    widget = forms.TextInput(attrs={'class': 'form-style', 'placeholder': 'Digite sua matrícula'}))

    password = forms.CharField(
    widget=forms.PasswordInput(attrs={'class': 'form-style', 'placeholder': 'Digite sua senha'}))

    checkBox = forms.BooleanField(required = False)


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
        user.set_password(self.cleaned_data['password'])
        user.username(self.cleaned_data['profile_registration'])
        
        if commit:
            user.save()
            Profile.objects.create(
                user=user, 
                profile_type = self.cleaned_data['profile_type'], 
                profile_registration = self.cleaned_data['profile_registration']
            )
            
        return user
            

class SchoolClassForm(forms.ModelForm):

    school_class_students_wid=forms.FileField()


    def clean(self):
        #pegando o valor padrão do clean
        cleaned_data=super().clean()

        #recebendo o arquivo do input
        temp_file=cleaned_data.get('school_class_students_wid')

        #verificando se existem erros  no input e criando um arquivo temporário
        if not self.has_error('school_class_students_wid'):
            schoolClass_file= NamedTemporaryFile()
        

        #escrevendo os dados do aquivo de upload no arquivo temporário
        with schoolClass_file as file:
            for chunk in temp_file.chunks():
                file.write(chunk)
            
            
            #adicionando o arquivo a cleaned_data
        cleaned_data['school_class_file']=schoolClass_file
        return cleaned_data
    def save(self,profile,commit=True):
        '''profile=request.user.profile on view'''
        self.instance.school_class_teacher=profile
        instance=super(SchoolClassForm,self).save(commit=False)

        if commit:
            relation=[]
            with open(self.cleaned_data.get('school_class_file').name,'r') as csv_file:
                    leitor=csv.DictReader(csv_file)

                    for r in leitor:

                        student=Student.objects.filter(student_registration=r['matricula']).first()
                        if student:
                            relation.append(student)
                        else:
                            Student.objects.create(student_name=r['nome'],student_registration=r['matricula'])
                            relation.append(student)

            #fechando o arquivo temporário e consequentemente o apagando
            self.cleaned_data.get('school_class_file').close()
            #salvando no db
            instance.save()
            #adicionando as relações
            instance.school_class_students.add(*relation)
        return instance
    
    class Meta:
        model=SchoolClass
        fields=['school_class_name']
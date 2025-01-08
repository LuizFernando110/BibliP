from django import forms 

class loginTeacherForm(forms.Form):
    teacherEnrollment = forms.CharField(max_length = 14,
    widget = forms.TextInput(attrs={'class': 'form-style', 'placeholder': 'Digite sua matrícula'}))

    password = forms.CharField(
    widget=forms.PasswordInput(attrs={'class': 'form-style', 'placeholder': 'Digite sua senha'}))

    checkBox = forms.BooleanField(required = False)

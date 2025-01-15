from django import forms 

class loginTeacherForm(forms.Form):
    teacherEnrollment = forms.CharField(max_length = 14,
    widget = forms.TextInput(attrs={'class': 'form-style', 'placeholder': 'Digite sua matrícula'}))

    password = forms.CharField(
    widget=forms.PasswordInput(attrs={'class': 'form-style', 'placeholder': 'Digite sua senha'}))

    checkBox = forms.BooleanField(required = False)


class userRegisterForm(forms.Form):
    account_type = forms.ChoiceField(choices = [('Servidor', 'Servidor'), ('Professor', 'Professor')], widget=forms.RadioSelect)

    name = forms.CharField(max_length = 100,
    widget = forms.TextInput(attrs={'class': 'form-style', 'placeholder': 'Digite seu nome'}))

    email = forms.EmailField(max_length = 100,
    widget = forms.EmailInput(attrs={'class': 'form-style', 'placeholder': 'Digite seu email'}))
    
    teacherEnrollment = forms.CharField(max_length = 14,
    widget = forms.TextInput(attrs={'class': 'form-style', 'placeholder': 'Digite sua matrícula'}))

    password = forms.CharField(
    widget=forms.PasswordInput(attrs={'class': 'form-style', 'placeholder': 'Digite sua senha'}))

    confirm_password = forms.CharField(
    widget=forms.PasswordInput(attrs={'class': 'form-style', 'placeholder': 'Confirme sua senha'}))


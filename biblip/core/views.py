from django.shortcuts import render,HttpResponse,redirect
from django.contrib import messages
from django.views.generic import ListView,DetailView,FormView,CreateView, FormView
from .forms import LoginForm, ProfileRegistrationForm,SchoolClassForm
from employee.models import Book,Borrow,Profile

from django.contrib.auth.models import User
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LogoutView
from django.shortcuts import redirect, get_object_or_404


class index(ListView):
    model=Book
    context_object_name='books'
    template_name='core/index.html'

    def get_queryset(self):
        search=self.request.GET.get('search')
        if search:
            queryset=Book.objects.filter(book_title__icontains=search)
            return queryset
        queryset=super().get_queryset()
        return queryset

def search(request,search):
    context={'search':search}

    #podemos reutilizar o Index.html nesta rota, mas prtimeiro precisamos da conexão com o banco de dados
    return render(request,"core/search_temp.html",context)



class details(DetailView):
    model=Book
    template_name='core/book_details.html'
    pk_url_kwarg='book_pk'
    context_object_name='book'

def borrow(request,book_pk):
    context={'book_pk':book_pk}
    return render(request,'core/book_borrow.html',context)


class borrow_history(ListView):
    model=Borrow
    template_name='core/borrow_history.html'
    context_object_name='borrow_history'

    def get_queryset(self):
        prof=self.request.user.profile
        queryset=Borrow.objects.filter(borrow_teacher=prof)
        return queryset

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['filter_title']='Histórico de alugueis'
        return context
    


class borrow_details(DetailView):
    template_name="employer_borrow_details.html"
    model=Borrow
    context_object_name='borrow'
    pk_url_kwarg='borrow_pk'


class ProfileRegistrationCreateView(CreateView):
    form_class = ProfileRegistrationForm
    model = User
    template_name = "core/user_register.html"
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        password = form.cleaned_data.get('password')
        confirm_password = form.cleaned_data.get('confirm_password')

        if password != confirm_password:
            form.add_erro('confirm_password', 'As senhas não são compatíveis.')
            return super().form_invalid(form)
        
        return super().form_valid(form)

class LoginView(FormView):
    template_name = 'core/login.html'  
    form_class = LoginForm


    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        remeber_me = form.cleaned_data['remember_me']


        user = authenticate(self.request, username=username, password=password)

        if user is not None:
            login(self.request, user)
            if remeber_me:
                self.request.session.set_expiry(2592000)
            else:
                self.request.session.set_expiry(0)
                
            return redirect(self.get_success_url(user))
        else:
            messages.error(self.request, "Usuário ou senha inválidos.")
            return self.form_invalid(form)  

    def get_success_url(self, user):
        try:
            profile = get_object_or_404(Profile, user=user)
            if profile.profile_type == 1:
                return reverse('borrow_management')
            else:
                return reverse('index')
        except Profile.DoesNotExist:
            logout(self.request)
            return reverse('login')
        
    
    def form_invalid(self, form):
        if not form.is_valid():
            messages.error(self.request, "Usuário ou senha incorreto")

        return self.render_to_response(self.get_context_data(form=form))

    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.get_success_url(request.user))
        return super().dispatch(request, *args, **kwargs)
    

class LogoutView(LogoutView):
    next_page = reverse_lazy('login')



class school_class_creation(FormView):
    form_class=SchoolClassForm
    template_name='core/class_register_modal.html'
    success_url=reversed('index')

    def form_valid(self, form):
        form.save(profile=self.request.user.profile)
        messages.add_message(self.request,messages.SUCCESS,"Turma adicionada com sucesso")
        return redirect('index')

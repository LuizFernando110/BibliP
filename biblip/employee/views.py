from django.shortcuts import render,HttpResponse
from django.views.generic import ListView,DetailView
from django.db.models.functions import ExtractMonth
#importançoes temporararias para o json:
import json
from django.conf import settings
import os
from .forms import bookRegisterForm
from .models import Book,Borrow,Genre
from datetime import datetime, timedelta
from core.views import search, split_columns

class borrow_management(ListView):
    model=Borrow
    template_name="employer_index.html"

    def get_context_data(self, **kwargs):
        
        Borrow.objects.annotate(month=ExtractMonth('borrow_delivery_date'))
        today = datetime.today()

        #calculando primeiro e último dia da semana
        #extractWeek usa sehunda como primeiro dia da semana, por isso está sendo feito manualmente
        day_of_week = (datetime.weekday(today)+1)%7 
        first_day_of_the_week=datetime.date(today-timedelta(days=day_of_week))
        last_day_of_the_week=datetime.date(today+timedelta(days=(6-day_of_week)))


        week_appointments=Borrow.objects.filter(borrow_delivery_date__range=(first_day_of_the_week,last_day_of_the_week))
        pending_appointments=Borrow.objects.filter(borrow_status=3)


        appointments_limit = 4
        hidden_week_appointments_count = max(len(week_appointments) - appointments_limit, 0)

        pending_limit = 4
        hidden_pending_count = max(len(pending_appointments) - pending_limit, 0)


        month_appointments=Borrow.objects.filter(borrow_delivery_date__month=ExtractMonth('borrow_delivery_date'))
        month_appointments=month_appointments.exclude(borrow_delivery_date__range=(first_day_of_the_week,last_day_of_the_week))
        hidden_month_appointments_count=max(len(month_appointments) - appointments_limit, 0)

        context = {
            'week_appointments': week_appointments[:appointments_limit], 
            'pending_appointments': pending_appointments[:pending_limit],
            'month_appointments':month_appointments[:appointments_limit],
            'hidden_week_appointments': hidden_week_appointments_count,
            'hidden_month_appointments': hidden_month_appointments_count,
            'hidden_pending': hidden_pending_count,
            'employer': True
        }
        return context

class books_management(ListView):
    model=Book
    context_object_name='books'
    template_name='books-management.html'

    def get_queryset(self):
        search=self.request.GET.get('search')
        books = Book.objects.all()

        if search:
            books = books.filter(book_title__icontains=search)

        
        return books  # Retorna apenas o queryset, sem adicionar outras variáveis


class employer_borrow_list(ListView):
    model=Borrow
    template_name='employer_borrow_list.html'

    def get_context_data(self, **kwargs):
        
        if self.request.method=='GET':
            Borrow.objects.annotate(month=ExtractMonth('borrow_delivery_date'))
            today = datetime.today()

            #calculando primeiro e último dia da semana
            #extractWeek usa sehunda como primeiro dia da semana, por isso está sendo feito manualmente
            day_of_week = (datetime.weekday(today)+1)%7 
            first_day_of_the_week=datetime.date(today-timedelta(days=day_of_week))
            last_day_of_the_week=datetime.date(today+timedelta(days=(6-day_of_week)))


            appointments=Borrow.objects.all()
            if self.request.GET.get('appointments_type')=='month':
                appointments=Borrow.objects.filter(borrow_delivery_date__month=ExtractMonth('borrow_delivery_date'))
                appointments=appointments.exclude(borrow_delivery_date__range=(first_day_of_the_week,last_day_of_the_week))
                
            
            if self.request.GET.get('appointments_type')=='week':
                appointments=Borrow.objects.filter(borrow_delivery_date__range=(first_day_of_the_week,last_day_of_the_week))

        return {'borrow_history':appointments,'employer':True}


class employer_borrow_details(DetailView):
    model=Borrow
    pk_url_kwarg='borrow_pk'  
    template_name='employer_borrow_details.html'
        


def create_book(request):
    return HttpResponse('<h1>Livro Criado!!</h1>')

def update_book(request):
    return HttpResponse('<h1>Livro Editado</h1>')

def delete_book(request):
    return HttpResponse('<h1>Livro Deletado</h1>')

def book_register(request):
    context = {'employer':True, 'form': bookRegisterForm()}
    return render(request, 'book_register.html', context)
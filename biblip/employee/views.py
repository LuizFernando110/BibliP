from django.shortcuts import render,HttpResponse
#importançoes temporararias para o json:
import json
from django.conf import settings
import os

def borrow_management(request):
    json_path_temp = os.path.join(settings.BASE_DIR, 'employee', 'appointment.json')
    with open (json_path_temp, 'r') as file:
        appointments = json.load(file)
    #Não esta acontecendo aqui mais a ideia é que o appointments seja os da semana, mas pendencias é entre todos 
    appointments_limit = 8
    hidden_appointments_count = max(len(appointments) - appointments_limit, 0)

    pending_appointments = [app for app in appointments if app.get('pendency')]

    pending_limit = 4
    hidden_pending_count = max(len(pending_appointments) - pending_limit, 0)

    context = {
        'appointments': appointments[:appointments_limit], 
        'pending_appointments': pending_appointments[:pending_limit],
        'hidden_appointments': hidden_appointments_count,
        'hidden_pending': hidden_pending_count,
        'employer': True
    }
    return render(request, 'index.html', context)


def employer_borrow_list(request):
    json_path_temp = os.path.join(settings.BASE_DIR, 'employee', 'appointment.json') 
    with open (json_path_temp, 'r') as file:
        borrow_history = json.load(file)

    context={'employer':True,
             'filter_title': 'Histórico de alugueis',
            'borrow_history': borrow_history}
    return render(request,'employer_borrow_list.html',context)


def employer_borrow_details(request,borrow_pk):
    json_path_temp = os.path.join(settings.BASE_DIR, 'core', 'borrow_history.json') 
    with open (json_path_temp, 'r') as file:
        borrow_history = json.load(file)

    context={'employer':True,
            'borrow_history': borrow_history}
    return render(request,'employer_borrow_details.html',context)

def create_book(request):
    return HttpResponse('<h1>Livro Criado!!</h1>')

def update_book(request):
    return HttpResponse('<h1>Livro Editado</h1>')

def delete_book(request):
    return HttpResponse('<h1>Livro Deletado</h1>')

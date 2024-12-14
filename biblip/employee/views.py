from django.shortcuts import render,HttpResponse
#importançoes temporararias para o json:
import json
from django.conf import settings
import os

def borrow_management(request):
    json_path_temp = os.path.join(settings.BASE_DIR, 'employee', 'appointment.json')
    with open (json_path_temp, 'r') as file:
        appointments = json.load(file)
    context = {'appointments': appointments, 'employer': True}
    return render(request, 'index.html', context)

def create_book(request):
    return HttpResponse('<h1>Livro Criado!!</h1>')

def update_book(request):
    return HttpResponse('<h1>Livro Editado</h1>')

def delete_book(request):
    return HttpResponse('<h1>Livro Deletado</h1>')

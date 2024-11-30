from django.urls import path
from .views import borrow_management,delete_book,update_book,create_book

urlpatterns = [
    path('employer/borrow_management',borrow_management,name='borrow_management'),
    path('employer/create_book',create_book,name='create_book'),
    path('employer/update_book',update_book,name='update_book'),
    path('employer/delete_book',delete_book,name='delete_book'),

]
from django.urls import path
from .views import index,search,details,borrow,borrow_history, login_teacher, borrow_details, user_register,school_class_creation, teste

urlpatterns = [
    path('',index.as_view(),name='index'),
    path('collection/<str:search>',search,name='search'),
    path('collection/details/<int:book_pk>',details.as_view(),name='details'),
    path('collection/borrow/<int:book_pk>',borrow,name='borrow'),
    path('collection/history/borrow_history',borrow_history,name='borrow_history'),
    path('collection/history/borrow_history/borrow_details/<int:borrow_pk>',borrow_details,name='borrow_history_details'),
    path('login',login_teacher,name='login_teacher'), 
    path('register',user_register,name='user_register'),
    path('profile/school_class/create',school_class_creation,name='school_class_creation'),
    path('teste',teste,name='teste'),
]
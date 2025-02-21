from django.urls import path
from .views import index,details,borrow,borrow_history, borrow_details, ProfileRegistrationCreateView, school_class_creation, LoginView, LogoutView
from .ajax_endpoints import cancel_borrow
urlpatterns = [
    path('',index.as_view(),name='index'),
    path('collection/details/<int:book_pk>',details.as_view(),name='details'),
    path('collection/borrow/<int:book_pk>',borrow.as_view(),name='borrow'),
    path('collection/history/borrow_history',borrow_history.as_view(),name='borrow_history'),
    path('collection/history/borrow_history/borrow_details/<int:borrow_pk>',borrow_details.as_view(),name='borrow_history_details'),
    path('login',LoginView.as_view(),name='login'), 
    path('logout', LogoutView.as_view(), name='logout'),
    path('register',ProfileRegistrationCreateView.as_view(),name='user_register'),
    path('profile/school_class/create',school_class_creation.as_view(),name='school_class_creation'),
    path('collection/borrow/<int:borrow_pk>/cancel', cancel_borrow,name='cancel_borrow'),
]
from .models import Borrow
from datetime import date

def borrow_close_evaluation(borrow:'Borrow'):
    return_status=4

    for student_borrow in borrow.borrowstudent_set.all():
        if student_borrow.borrow_student_status==2: 
            student_borrow.borrow_student_status=4
            return_status=3
            student_borrow.save()
        elif student_borrow.borrow_student_status==1:
            student_borrow.borrow_student_status=6
            student_borrow.save()
    borrow.borrow_status=return_status
    print(borrow.borrow_status)
    borrow.save()
    return borrow

def evaluate_all_by_date():
    borrows_elatuate=Borrow.objects.filter(borrow_delivery_date__lt=date.today()).filter(borrow_status__in=[2,3])
    for borrow in borrows_elatuate:
        borrow_close_evaluation(borrow)

from .models import Borrow

def borrow_close_evaluation(borrow:'Borrow'):
    return_status=4

    for student_borrow in borrow.borrowstudent_set.all():
        if student_borrow.borrow_student_status==2: 
            student_borrow.borrow_student_status=4
            student_borrow.save()
            return_status=3
        elif student_borrow.borrow_student_status==1:
            student_borrow.borrow_student_status=6
            student_borrow.save()
    borrow.borrow_status=return_status
    borrow.save()
    return borrow

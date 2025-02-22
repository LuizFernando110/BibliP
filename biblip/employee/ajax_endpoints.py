from django.http import JsonResponse
from employee.models import Borrow, BorrowStudent
from employee.borrow_evaluations import borrow_close_evaluation
from datetime import date


def cancel_borrow(request,borrow_pk):
    borrow=Borrow.objects.get(id=borrow_pk)
    if request.user.profile==borrow.borrow_teacher and borrow.borrow_status not in [3,4]:
        

        borrow = borrow_close_evaluation(borrow)
        borrow.borrow_delivery_date=date.today()

        borrow.save()
        
        book=borrow.borrow_book
        book.book_status=1
        book.save()

        return JsonResponse({
            
            'success':True,
            'borrow':{
                'data_entrega':borrow.borrow_delivery_date.strftime('%d/%m/%Y'),
            }
        })
    else:
        return JsonResponse({
            'success':False,
        })
    
def accept_borrow(request,borrow_pk):
    borrow=Borrow.objects.get(id=borrow_pk)
    if borrow.borrow_status ==1:
        borrow.borrow_status=2
        borrow.save()

        
        return JsonResponse({
            
            'success':True,
        })
    else:
        return JsonResponse({
            'success':False,
        })

def student_borrow_receipt(request,borrow_student_pk):
    borrow_student=BorrowStudent.objects.get(id=borrow_student_pk)


    if borrow_student.borrow_student_status==1:
        borrow_student.borrow_student_status=2
        borrow_student.save()

        return JsonResponse({
            
            'success':True,
        })
    else:
        return JsonResponse({
            'success':False,
        })
    
def student_borrow_deliver(request,borrow_student_pk):
    borrow_student=BorrowStudent.objects.get(id=borrow_student_pk)
    book=borrow_student.borrow_holder.borrow_book
    if borrow_student.borrow_student_status==2:
        borrow_student.borrow_student_status=3
        borrow_student.save()

        book.number_available+=1
        book.save()
        return JsonResponse({
                
                'success':True,
            })
    
    elif borrow_student.borrow_student_status==4:
        borrow_student.borrow_student_status=5
        borrow_student.save()
        book.number_available+=1
        book.save()
        return JsonResponse({
            
            'success':True,
        })
    else:
        return JsonResponse({
            'success':False,
        })
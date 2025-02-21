from django.http import JsonResponse
from employee.models import Borrow
from employee.borrow_evaluations import borrow_close_evaluation
from datetime import date,timedelta


def cancel_borrow(request,borrow_pk):
    borrow=Borrow.objects.get(id=borrow_pk)
    if request.user.profile==borrow.borrow_teacher and borrow.borrow_status not in [3,4]:
        

        borrow = borrow_close_evaluation(borrow)
        borrow.borrow_delivery_date=date.today()

        borrow.save()
        
        
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
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse


def is_employer(function,redirect_name='login'):
  def wrapper(request, *args, **kw):
    if request.user.is_anonymous:
      return HttpResponseRedirect(reverse(redirect_name))
   
    profile=request.user.profile

    if not (profile.profile_type==1):
      return HttpResponseRedirect(reverse(redirect_name))
    else:
      return function(request, *args, **kw)
  return wrapper
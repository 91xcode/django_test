# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,render_to_response

# Create your views here.


from django.http import HttpResponse
 
 
def lists(request):
    return HttpResponse(u"欢迎光临 自强学堂!")



def list(request):

    host = request.GET.get('host', '')
    return render_to_response("crash/home.html", locals())

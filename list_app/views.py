from django.shortcuts import render
from django.http import HttpResponse
from models import ListEntry, OwnerEntry

# Create your views here.

def login_success(request):
    # u = OwnerEntry(name=request.user)
    # print(u.name)
    # print(u.lists)
    # if(u == None):
    #     print("no lists for user")
    # else:
    #     print(u.listentry_set.all())

    records = OwnerEntry.objects.filter(name=request.user)
    if(records == None):
        print("no lists for:")
        print(request.user)
    else:
        for oe in records:
            print(oe.list.name)

    return HttpResponse("login success!")

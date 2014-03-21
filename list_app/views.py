from django.shortcuts import render
from django.http import HttpResponse
from models import ListEntry, OwnerEntry
from django.template import RequestContext, loader

# Create your views here.

def login_success(request):
    # u = OwnerEntry(name=request.user)
    # print(u.name)
    # print(u.lists)
    # if(u == None):
    #     print("no lists for user")
    # else:
    #     print(u.listentry_set.all())
    output = 'nothing'
    records = OwnerEntry.objects.filter(name=request.user)
    if(records == None):
        print("no lists for:")
        print(request.user)
    else:

        for oe in records:
            print(oe.list.name)

        output = ', '.join(r.list.name for r in records)
        template = loader.get_template('app/login_success.html')
        context = RequestContext(request, {
            'user_email_list': records,
        })
        return HttpResponse(template.render(context))

    return HttpResponse(output)

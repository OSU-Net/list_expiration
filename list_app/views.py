from django.shortcuts import render
from django.http import HttpResponse
from models import ListEntry, OwnerEntry
from django.template import RequestContext, loader

# Create your views here.

def login_success(request):

    output = str(None)
    oe_records = OwnerEntry.objects.filter(name=request.user)
    lists = []
    for oe in oe_records:
        lists.append(oe.list)

    if(oe_records == None):
        print("no lists for:")
        print(request.user)
    else:


        output = ', '.join(r.list.name for r in oe_records)
        template = loader.get_template('login_success.html')
        context = RequestContext(request, {
            'lists': lists,
        })
        return HttpResponse(template.render(context))

    return HttpResponse(output)

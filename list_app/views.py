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

    if not oe_records:
        return HttpResponse(str.format("no lists for {0}", request.user))
    else:

        template = loader.get_template('login_success.html')
        context = RequestContext(request, {
            'lists': lists,
        })
        return HttpResponse(template.render(context))


def list_edit(request, admin_name, list_id):
    admin_lists = OwnerEntry.objects.filter(name=admin_name)

    list_to_edit = None
    for l in admin_lists:
        if l.id == list_id:
            list_to_edit = l

    if not list_to_edit:
        return HttpResponse(str.format("user {0} is not an administrator of {1}", admin_name, list_to_edit.name))

    template = loader.get_template('list_edit.html')
    context = RequestContext(request, {
        ''
    })

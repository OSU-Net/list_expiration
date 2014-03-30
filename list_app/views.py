from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from models import ListEntry, OwnerEntry
from django.template import RequestContext, loader

# Create your views here.


def login_success(request):
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
            'admin_name': request.user
        })
        return HttpResponse(template.render(context))


def list_edit(request):
    if request.method == "POST":  # changes to a list have been submitted, TODO: check the validity of submitted data
        return HttpResponseRedirect("app/login_success")
    else:
        admin_name = request.GET['admin_name']
        list_id = request.GET['list_id']

        print(list_id)
        print(admin_name)
        #^^ these two lines could possibly cause a key error

        admin_lists = ListEntry.objects.filter(name=admin_name)
        list_to_edit = ListEntry.objects.filter(id=list_id)
        # list_to_edit = None
        # for l in admin_lists:
        #     if l.id == list_id:
        #         list_to_edit = l

        if not list_to_edit:
            return HttpResponse(str.format("user {0} is not an administrator of {1}", admin_name, list_to_edit.name))

        template = loader.get_template('list_edit.html')
        context = RequestContext(request, {
            'list_to_edit': list_to_edit
        })

        return HttpResponse(template.render(context))

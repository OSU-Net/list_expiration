from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from models import ListEntry, OwnerEntry
from django.template import RequestContext, loader
from django.contrib.auth.models import User

#view for the page that is redirected to after successful CAS authentication
def list_index(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('login')

    user_lists = OwnerEntry.objects.filter(name=request.user)
    lists = []
    for list_record in user_lists:
        lists.append(list_record.list)

    if not user_lists:
        return HttpResponse(str.format("no lists for {0}", request.user))

    else:
        template = loader.get_template('list_index.html')
        context = RequestContext(request, {
            'lists': lists,
            'admin_name': request.user
        })
        return HttpResponse(template.render(context))


def validate_list_changes():
    return "success"


def list_edit(request):
    if request.method == "POST":  # changes to a list have been submitted, TODO: check the validity of submitted data
        error_msg = validate_list_changes()

        if error_msg == 'success':
            return HttpResponseRedirect("lists/index")
        else:
            #render list_edit.html with a mean-looking red warning
            return HttpResponse("hello world!")
    else:
        admin_name = request.GET['admin_name']
        list_id = request.GET['list_id']

        list_to_edit = ListEntry.objects.filter(id=list_id)

        if not list_to_edit:
            return HttpResponse(str.format("user {0} is not an administrator of {1}", admin_name, list_to_edit.name))
            # ^^ I don't think this will ever be executed...

        template = loader.get_template('list_edit.html')
        context = RequestContext(request, {
            'admin_name': admin_name,
            'list_to_edit': list_to_edit,
            'invalid_edit': False,
        })

        return HttpResponse(template.render(context))

def list_edit_cancel(request):

    template = loader.get_template('list_edit.html')

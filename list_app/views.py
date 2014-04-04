from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from models import ListEntry, OwnerEntry
from django.template import RequestContext, loader
from django.contrib.auth.models import User
from list_app.forms import list_edit_form
from datetime import *

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


def parse_expire_date(date_str):
    date_elements = str.split(date_str, '-')


    if len(date_elements) != 3:
        return None
    else:
        return datetime(int(date_elements[2]), int(date_elements[0]), int(date_elements[1]))


def validate_list_changes(cd):
    try:
        list_id = cd['list_id']
        admin_name = cd['expire_date']
        return True

    except object:
        print(str.format("Exception of type {0} occurred because invalid list form data was submitted",
                         type(object)))
        return False


def list_edit(request):
    if request.method == "POST":  # changes to a list have been submitted, TODO: check the validity of submitted data
        edit_form = list_edit_form(request.POST)
        result_message = str(None)

        if edit_form.is_valid() and validate_list_changes(edit_form.cleaned_data):
            cd = edit_form.cleaned_data
            le = ListEntry.objects.filter(id=cd['list_id'])
            le.expire_date = parse_expire_date(cd['expire_date'])
            le.save()

            #TODO: redirect to index page and display some sort of message indicating successful changes
            return HttpResponseRedirect('lists/index')

        else:
            #return an error message
            return HttpResponse(str.format("Errors:\n {0} \n {1}", edit_form['list_id'].errors, edit_form['expire_date'].errors))



        # if error_msg == 'success':
        #     #edit the list and redirect to index
        #     return HttpResponseRedirect("lists/index")
        # else:
        #     #render list_edit.html with a mean-looking red warning
        #     return HttpResponse("hello world!")
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
            'list_id': list_id,
            'invalid_edit': False,
        })

        return HttpResponse(template.render(context))


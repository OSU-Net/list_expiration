from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from models import ListEntry, OwnerEntry
from django.template import RequestContext, loader
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from list_app.forms import ListEditForm
from datetime import *


#view for the page that is redirected to after successful CAS authentication
# @csrf_exempt
def list_index(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('login')

    print('hello!')
    user_entries = OwnerEntry.objects.filter(name=request.user)

    lists = []
    user_list_ids = []
    user_lists = []

    for user in user_entries:
        user_list_ids.append(user.list_id)

    user_lists = ListEntry.objects.filter(id__in=user_list_ids)

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

def validate_list_changes(cd):
    try:
        list_id = cd['list_id']
        expire_date = cd['expire_date']
        return True

    except object:
        print(str.format("Exception of type {0} occurred because invalid list form data was submitted",
                         type(object)))
        return False


# @csrf_exempt
def submit_list_edit(request):
    edit_form = ListEditForm(request.POST)

    if edit_form.is_valid() and validate_list_changes(edit_form.cleaned_data):
        cd = edit_form.cleaned_data
        le = ListEntry.objects.get(id=cd['list_id'])
        le.expire_date = cd['expire_date']
        le.save()

    else:
        #this 'else statement should never be executed, if it does, it means that the browser submitted
        #edits that are invalid
        return HttpResponse("ERROR: Server rejected list changes.")

    return HttpResponseRedirect('/lists/index')

def list_edit(request):
    if request.method == "POST":  # changes to a list have been submitted, TODO: check the validity of submitted data
        edit_form = ListEditForm(request.POST)

        if edit_form.is_valid() and validate_list_changes(edit_form.cleaned_data):
            cd = edit_form.cleaned_data
            le = ListEntry.objects.get(pk=cd['list_pk'])
            le.expire_date = cd['expire_date']
            le.save()

            #TODO: redirect to index page and display some sort of message indicating successful changes
            return HttpResponseRedirect('lists/index')

        else:
            #return an error message
            return HttpResponse(str.format("Errors:\n {0} \n {1}", edit_form['list_pk'].errors, edit_form['expire_date'].errors))

    else:
        admin_name = request.GET['admin_name']
        list_pk = request.GET['list_pk']

        list_to_edit = ListEntry.objects.get(id=list_pk)

        if not list_to_edit:
            return HttpResponse(str.format("user {0} is not an administrator of {1}", admin_name, list_to_edit.name))
            # ^^ I don't think this will ever be executed...

        template = loader.get_template('list_edit.html')
        context = RequestContext(request, {
            'admin_name': admin_name,
            'list_pk': list_pk,
            'list_expire_date': list_to_edit.expire_date,
            'invalid_edit': False,
        })

        return HttpResponse(template.render(context))


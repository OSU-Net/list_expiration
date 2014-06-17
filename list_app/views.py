from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from list_app.models import * 
from django.template import RequestContext, loader
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt

from list_app import urls
from list_app.forms import ListEditForm
import datetime

import pdb

def onid_transition(request):
    user_code = request.GET.get('id', '')
    
    if user_code == '':
        raise Http404   
    
    #when the user redirects here after authenticating through CAS, fill the entry for their ONID email
    authenticated = False

    if request.user.is_authenticated():
        # owner = OldOwner.objects.get(link_code=user_code)
        # owner.onid_email = request.user.username + "@onid.oregonstate.edu";
        # owner.save()

        pdb.set_trace()

        #set the automatic expire date to be two years out
        old_owner = OldOwner.objects.get(link_code=user_code)
        #owner = ListEntry(create_date=old_owner.
        owner_lists = old_owner.lists.all()
        for l in owner_lists:

            ls = ListEntry.objects.filter(name=l.name)
            if ls.exists():
                if not OwnerEntry.objects.filter(lists__name=l.name, name=request.user.username).exists():
                    oe = OwnerEntry(name=request.user.username, lists=ls)
                    oe.save()
            else:
                ls = ListEntry(name=l.name, 
                               create_date=l.create_date, 
                               expire_date=l.create_date + datetime.timedelta(365 * 2)) # set expiration out two days
                ls.save()

        #redirect to the expiration home page
        return redirect('list_app:list_index')

    try:
        owner = OldOwner.objects.get(link_code=user_code)
    except OldOwner.DoesNotExist:
       raise Http404

    template = loader.get_template('onid_transition.html')
    context = RequestContext(request, {
        'lists': owner.lists.all(),
        'authenticated': authenticated,
    })
    return HttpResponse(template.render(context))

#view for the page that is redirected to after successful CAS authentication
def list_index(request):

    if not request.user.is_authenticated():
        return HttpResponseRedirect('login')

    #user_entries = OwnerEntry.objects.filter(name=request.user)
    try:
        lists = OwnerEntry.objects.get(name=request.user.username).lists.all()

    except OwnerEntry.DoesNotExist:
        return HttpResponse(str.format("no lists for {0}", request.user))
    
    template = loader.get_template('list_index.html')
    context = RequestContext(request, {
        'lists': lists,
        'admin_name': request.user.username
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


from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseBadRequest
from list_app.models import * 
from django.template import RequestContext, loader
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse

from list_app import urls
from list_app.list_status import * 
from list_app.forms import ListEditForm

from list_site import settings

from django_cas.views import login

import datetime, subprocess

import pdb
from list_site.verify_cas import verify_cas2


def no_onid(request):
    user_code = request.GET.get('id', '')
    list_name = request.GET.get('list_name', '')
    action = request.GET.get('action', '')
     
    if user_code == '':
        raise Http404
    
    if list_name == '':
        raise Http404
    
    if action == 'delete': #delete the list and return the user to onid transition page
        #####....
        #remove the list from mailman, and mark it as deleted in the db
        old_list = OldList.objects.get(name=list_name)

        cmd_str = "list_app/management/commands/remove_list {0} {1} {2}". \
                  format(old_list.name,
                         settings.MAILMAN_LISTS_DIR,
                         settings.MAILMAN_SCRIPTS_DIR)
        subprocess.call(cmd_str, shell=True)
        old_list.deleted = True
        old_list.save()

        return HttpResponseRedirect(reverse('list_app:onid_transition') + 
            '?id=' + user_code)
           
    try:
        owner = OldOwner.objects.get(link_code=user_code)
        list = OldList.objects.get(name=list_name)
    except OldOwner.DoesNotExist, OldList.DoesNotExist:
        raise Http404

    this_owner = OldOwner.objects.get(link_code=user_code)
    list = OldList.objects.get(name=list_name) 

    owners = OldOwner.objects.filter(lists__name=list.name)
    list_status = ListStatus(list.name, [])

    for owner in owners:
        
        if not (owner.owner_email == this_owner.owner_email): 
            status = calc_owner_status(owner)
            list_status.owners.append(OwnerStatus(owner.owner_email, status))
    
    template = loader.get_template('no_onid.html')
    context = RequestContext(request, {
        'list_status': list_status
    })
    return HttpResponse(template.render(context))

def onid_transition(request):
    user_code = request.GET.get('id', '')
    
    if user_code == '':
        raise Http404   
    
    try:
        owner = OldOwner.objects.get(link_code=user_code)
    except OldOwner.DoesNotExist:
       raise Http404

    #when the user redirects here after authenticating through CAS, fill the entry for their ONID email
    authenticated = False

    if request.user.is_authenticated():

        # make sure that the authenticated onid user is not 
        #already entered as an owner to prevent duplicate owner entries
        if Owner.objects.filter(name=request.user.username).exists():

            logout(request)

            template = loader.get_template('onid_transition.html')
            context = RequestContext(request, {
                'lists': owner.lists.all(),
                'authenticated': authenticated,
                'error': 'This ONID account is already registered as a list owner.',
            })
            return HttpResponse(template.render(context))


        #set the automatic expire date to be two years out
        old_owner = OldOwner.objects.get(link_code=user_code)

        #create the Owner object
        new_owner = Owner(name=request.user.username)
        new_owner.save()

        #create relation for each list new owner is a part of
        old_lists = old_owner.lists.all()
        for l in old_lists:

            new_list = None

            #if a List hasnt been created do so and automatically set the expiration date out two years
            try:
                new_list = List.objects.get(name=l.name)
            except List.DoesNotExist:
                new_list = List(name=l.name, 
                                   create_date=l.create_date, 
                                   expire_date=l.create_date + datetime.timedelta(365 * 2))
                new_list.save()

            new_owner.lists.add(new_list)
            new_owner.save()
        
        #modify the 'OldOwner' entry so that other prospective list 
        #owners can see that this user has claimed ONID ownership of the list
        old_owner = OldOwner.objects.get(link_code=user_code)
        old_owner.onid_email = request.user.username
        old_owner.save()
        
        #redirect to the expiration home page
        return redirect('list_app:list_index')

    template = loader.get_template('onid_transition.html')
    context = RequestContext(request, {
        'lists': owner.lists.all(),
        'authenticated': authenticated,
        'user_code': user_code,
    })
    return HttpResponse(template.render(context))

#view for the page that is redirected to after successful CAS authentication
def list_index(request):

    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('cas_login'))

    #user_entries = Owner.objects.filter(name=request.user)
    try:
        lists = Owner.objects.get(name=request.user.username).lists.all()
    except Owner.DoesNotExist:
        #return HttpResponse(str.format("no lists for {0}", request.user))
        lists = None

    template = loader.get_template('list_index.html')
    context = RequestContext(request, {
        'lists': lists,
        'user_name': request.user.username
    })
    return HttpResponse(template.render(context))

def validate_list_changes(cd):
    try:
        list_id = cd['list_id']
        expire_date = cd['expire_date']
        return True

    except object:
        print(str.format("Exception of type {0} occurred because" +  
                         "invalid list form data was submitted",
                         type(object)))
        return False


# @csrf_exempt
def submit_list_edit(request):
    edit_form = ListEditForm(request.POST)

    if edit_form.is_valid() and validate_list_changes(edit_form.cleaned_data):
        cd = edit_form.cleaned_data
        le = List.objects.get(id=cd['list_id'])
        le.expire_date = cd['expire_date']
        le.save() 

    else:
        #this 'else statement should never be executed, if it does, it means that the browser submitted
        #edits that are invalid

        return HttpResponse("ERROR: Server rejected list changes.")

    return HttpResponseRedirect('/lists/index')

def list_edit(request):
    if request.method == "POST":  # changes to a list have been submitted 
        edit_form = ListEditForm(request.POST)

        if edit_form.is_valid() and validate_list_changes(edit_form.cleaned_data):
            cd = edit_form.cleaned_data
            le = List.objects.get(pk=cd['list_pk'])
            le.expire_date = cd['expire_date']
            le.save()

            #TODO: redirect to index page and display some sort of message indicating successful changes
            return HttpResponseRedirect('lists/index')

        else:
            #return an error message
            return HttpResponse(str.format("Errors:\n {0} \n {1}", 
                                edit_form['list_pk'].errors, 
                                edit_form['expire_date'].errors))

    else:
        admin_name = request.GET['admin_name']
        list_pk = request.GET['list_pk']

        list_to_edit = List.objects.get(id=list_pk)

        if not list_to_edit:
            return HttpResponse(str.format("user {0} is not an administrator of {1}", 
                                admin_name, 
                                list_to_edit.name))
            # ^^ I don't think this will ever be executed...

        template = loader.get_template('list_edit.html')
        context = RequestContext(request, {
            'admin_name': admin_name,
            'list_pk': list_pk,
            'list_expire_date': list_to_edit.expire_date,
            'invalid_edit': False,
        })

        return HttpResponse(template.render(context))

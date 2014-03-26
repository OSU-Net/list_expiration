from django import forms


class list_edit(forms.Form):
    expire_date = forms.DateField(required=False)
    activate_date = forms.DateField()
    name = forms.CharField(max_length=64, required=False) #toying with the idea of allowing administrators to edit list names
    #this could possibly be problematic so this is just here for some code eye candy

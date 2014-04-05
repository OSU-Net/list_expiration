from django import forms
from datetime import *


class list_edit_form(forms.Form):
    expire_date = forms.DateTimeField(required=True)
    list_pk = forms.IntegerField()

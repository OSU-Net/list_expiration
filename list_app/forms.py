from django import forms
from datetime import *


class list_edit_form(forms.Form):
    expire_date = forms.CharField(required=True)
    list_id = forms.IntegerField()

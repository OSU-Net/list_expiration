from django import forms
from datetime import *


class ListEditForm(forms.Form):
    expire_date = forms.DateTimeField(required=True)
    list_id = forms.IntegerField(required=True)

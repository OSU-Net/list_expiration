from django import forms
from datetime import *

class list_edit(forms.Form):
    expire_date = forms.DateField(required=False)
    # activate_date = forms.DateField(required=False)
    name = forms.CharField(max_length=64, required=False) #toying with the idea of allowing administrators to edit list names
    # admins = forms.CharField(max_length=256, required=False)

    def is_valid(self):
        if self.expire_date < datetime.now():
            return False

        return True

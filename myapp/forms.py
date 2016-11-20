from django import forms
from .models import Input, COMMUNITYAREA

class InputForm(forms.ModelForm):

    attrs = {'class ' : 'form−control ',
             'onchange ' : 'this.form.submit() '}

    communityarea = forms.ChoiceField(choices=COMMUNITYAREA, required=True,
                              widget=forms.Select(attrs = attrs))
    class Meta:

        model = Input
        fields = ['communityarea']

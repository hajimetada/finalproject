from django import forms
from .models import Input, COMMUNITYAREAS

class InputForm(forms.ModelForm):

    attrs = {'class ' : 'form−control ',
             'onchange ' : 'this.form.submit() '}

    communityarea = forms.ChoiceField(choices=COMMUNITYAREAS, required=True,
                              widget=forms.Select(attrs = attrs))
    class Meta:

        model = Input
        fields = ['communityarea']

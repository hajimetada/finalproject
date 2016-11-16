from django import forms
from .models import Input, NEIGHBORHOODS

class InputForm(forms.ModelForm):

    attrs = {'class ' : 'form−control ',
             'onchange ' : 'this.form.submit() '}

    neighborhood = forms.ChoiceField(choices=NEIGHBORHOODS, required=True,
                              widget=forms.Select(attrs = attrs))
    class Meta:

        model = Input
        fields = ['neighborhood']

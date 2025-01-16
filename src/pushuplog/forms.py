from django import forms


class SimplePushupLogForm(forms.Form):
    sets = forms.IntegerField(min_value=0, initial=1)
    repetitions = forms.IntegerField(min_value=0, initial=10)

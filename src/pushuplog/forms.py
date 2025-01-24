from datetime import datetime
from django import forms


class SimplePushupLogForm(forms.Form):
    repetitions = forms.IntegerField(min_value=0, initial=10)
    when = forms.SplitDateTimeField(initial=datetime.now, required=False)

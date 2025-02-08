from datetime import datetime

from django import forms
from django.urls import reverse
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Row, Column, Submit, Reset, Button
from crispy_bootstrap5.bootstrap5 import FloatingField


class PushupLogForm(forms.Form):
    repetitions = forms.IntegerField(min_value=0, initial=10)
    when = forms.DateTimeField(initial=datetime.now, required=False)

    def __init__(self, *args, **kwargs):
        full_form = kwargs.pop("full_form", False)

        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.attrs["hx-target"] = "this"
        self.helper.layout = Layout(
            Row(
                FloatingField("repetitions", wrapper_class="gx-1 col-md-6"),
                FloatingField("when", wrapper_class="gx-1 col-md-6"),
            ),
            Div(
                Submit(
                    "submit",
                    "Submit",
                    hx_post=reverse("savelogentry"),
                    hx_swap="outerHTML",
                ),
                Reset("reset", "Reset", css_class="btn-secondary"),
            ),
        )

        if not full_form:
            self.helper.layout[0][1] = Column(
                Button(
                    "full_form",
                    "Set date and time",
                    css_class="btn-outline-primary fst-italic btn-sm",
                    hx_post=reverse("logentryform_full"),
                    hx_swap="outerHTML",
                ),
                css_class="col-md-6 d-md-flex align-items-center mb-3",
            )

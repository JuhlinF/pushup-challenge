from datetime import datetime

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Row, Column, Submit, Reset, Button
from crispy_bootstrap5.bootstrap5 import FloatingField


class PushupLogForm(forms.Form):
    repetitions = forms.IntegerField(min_value=0, initial=10)
    when = forms.DateTimeField(initial=datetime.now, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                FloatingField("repetitions", wrapper_class="gx-1 col-md-6"),
                FloatingField("when", wrapper_class="gx-1 col-md-6"),
            ),
            Div(
                Submit("submit", "Submit"),
                Reset("reset", "Reset", css_class="btn-secondary"),
            ),
        )

        self.simple_helper = FormHelper()
        self.simple_helper.layout = self.helper.layout
        self.simple_helper.layout[0][1] = Column(
            Button(
                "show_when",
                "Set date and time",
                css_class="btn-outline-primary fst-italic btn-sm",
                hx_get="?show_when=1",
                hx_target="#replace_div",
                hx_swap="outerHTML",
            ),
            css_class="col-md-6 d-md-flex align-items-center mb-3",
            id="replace_div",
        )

        self.when_helper = FormHelper()
        self.when_helper.form_tag = False
        self.when_helper.add_layout(
            Layout(
                FloatingField("when", wrapper_class="gx-1 col-md-6"),
            )
        )

        self.helper.attrs = self.simple_helper.attrs = {"hx_boost": "true"}

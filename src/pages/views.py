from django.http import HttpRequest
from django.shortcuts import render

from pushuplog.models import PushupLogEntry
from pushuplog.forms import SimplePushupLogForm


def home(request: HttpRequest):
    if request.method == "POST":
        form = SimplePushupLogForm(request.POST)
        if form.is_valid():
            sets = form.cleaned_data["sets"]
            reps = form.cleaned_data["repetitions"]
            if request.user.is_authenticated:
                user = request.user
            else:
                user = None
            PushupLogEntry.objects.create(user=user, sets=sets, repetitions=reps)

    form = SimplePushupLogForm()

    pushup_log = PushupLogEntry.objects.all()
    context = {
        "form": form,
        "pushup_log": pushup_log,
    }
    return render(request, "home.html", context)

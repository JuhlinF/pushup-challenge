from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from pushuplog.models import PushupLogEntry
from pushuplog.forms import SimplePushupLogForm


def index(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect("home")

    return render(request, "index.html")


@login_required
def home(request: HttpRequest):
    if request.method == "POST":
        form = SimplePushupLogForm(request.POST)
        if form.is_valid():
            sets = form.cleaned_data["sets"]
            reps = form.cleaned_data["repetitions"]
            user = request.user
            PushupLogEntry.objects.create(user=user, sets=sets, repetitions=reps)

    form = SimplePushupLogForm()

    pushup_log = PushupLogEntry.objects.filter(user=request.user).order_by("-when")
    context = {
        "form": form,
        "pushup_log": pushup_log,
    }
    return render(request, "home.html", context)

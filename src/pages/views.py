from datetime import date
import math

from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models import Sum
from django.db.models.functions import Coalesce

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
            reps = form.cleaned_data["repetitions"]
            when = form.cleaned_data["when"]
            user = request.user
            PushupLogEntry.objects.create(user=user, repetitions=reps, when=when)
            form = (
                SimplePushupLogForm()
            )  # Empty form to log new entry - if the form was invalid we re-show the previous form with error messages
    else:
        form = SimplePushupLogForm()

    pushup_log = PushupLogEntry.objects.filter(user=request.user).order_by("-when")
    context = {
        "form": form,
        "pushup_log": pushup_log,
    }

    # Calculate stats
    end_date = date(2026, 1, 1)
    today = date.today()

    statistics = {}
    statistics["goal"] = 50_000
    statistics.update(
        PushupLogEntry.objects.filter(user=request.user, when__date=today).aggregate(
            done_today=Coalesce(Sum("repetitions"), 0)
        )
    )
    statistics.update(
        PushupLogEntry.objects.filter(
            user=request.user, when__date__lt=today
        ).aggregate(done_before_today=Coalesce(Sum("repetitions"), 0))
    )
    statistics.update(
        PushupLogEntry.objects.filter(user=request.user).aggregate(
            done_total=Coalesce(Sum("repetitions"), 0)
        )
    )
    statistics["needed_day"] = math.ceil(
        (statistics["goal"] - statistics["done_before_today"]) / (end_date - today).days
    )
    statistics["left_today"] = statistics["needed_day"] - statistics["done_today"]

    context["statistics"] = statistics
    return render(request, "home.html", context)

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
    context = {}

    if request.htmx:
        context["form"] = SimplePushupLogForm()
        context["show_when_field"] = True
        return render(request, "components/logform.html", context)
    if request.method == "POST":
        form = SimplePushupLogForm(request.POST)
        if form.is_valid():
            kw = {
                "repetitions": form.cleaned_data["repetitions"],
                "user": request.user,
            }
            if form.cleaned_data["when"]:
                kw["when"] = form.cleaned_data["when"]
            PushupLogEntry.objects.create(**kw)

            form = (
                SimplePushupLogForm()
            )  # Empty form to log new entry - if the form was invalid we re-show the previous form with error messages
    else:
        form = SimplePushupLogForm()

    context["form"] = form

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


@login_required
def logs(request: HttpRequest):
    if request.method == "POST":
        id_to_delete = int(request.POST["entry_id"])
        logentry = PushupLogEntry.objects.get(id=id_to_delete)
        if logentry.user == request.user:
            logentry.delete()

    pushup_log = PushupLogEntry.objects.filter(user=request.user).order_by("-when")

    context = {
        "pushup_log": pushup_log,
    }

    return render(request, "logs.html", context)

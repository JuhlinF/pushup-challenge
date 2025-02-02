from datetime import date
import math

from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models import Sum
from django.db.models.functions import Coalesce

from pushuplog.models import PushupLogEntry
from pushuplog.forms import FullPushupLogForm
from users.models import User


def index(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect("home")

    return render(request, "index.html")


@login_required
def home(request: HttpRequest) -> HttpResponse:
    context = {}

    if request.htmx:
        context["form"] = FullPushupLogForm(
            {"repetitions": get_latest_reps(request.user) or 10}
        )
        if request.GET.get("show_when"):
            context["show_when_field"] = True
        return render(request, "components/logform.html", context)

    if request.method == "POST":
        form = FullPushupLogForm(request.POST)
        if form.is_valid():
            kw = {
                "repetitions": form.cleaned_data["repetitions"],
                "user": request.user,
            }
            if form.cleaned_data["when"]:
                kw["when"] = form.cleaned_data["when"]
            new_entry = PushupLogEntry.objects.create(**kw)
            context["new_entry"] = new_entry
            form = None
    else:
        form = FullPushupLogForm({"repetitions": get_latest_reps(request.user) or 10})

    statistics = get_statistics(request.user)

    context["form"] = form
    context["statistics"] = statistics
    return render(request, "home.html", context)


@login_required
def logs(request: HttpRequest) -> HttpResponse:
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


def get_latest_reps(user: User) -> int | None:
    try:
        latest_reps = (
            PushupLogEntry.objects.filter(user=user).latest("when").repetitions
        )
    except PushupLogEntry.DoesNotExist:
        latest_reps = None

    return latest_reps


def get_statistics(user: User) -> dict:
    # Calculate stats
    end_date = date(2026, 1, 1)
    today = date.today()

    statistics = {}
    statistics["goal"] = 50_000
    statistics.update(
        PushupLogEntry.objects.filter(user=user, when__date=today).aggregate(
            done_today=Coalesce(Sum("repetitions"), 0)
        )
    )
    statistics.update(
        PushupLogEntry.objects.filter(user=user, when__date__lt=today).aggregate(
            done_before_today=Coalesce(Sum("repetitions"), 0)
        )
    )
    statistics.update(
        PushupLogEntry.objects.filter(user=user).aggregate(
            done_total=Coalesce(Sum("repetitions"), 0)
        )
    )
    statistics["needed_day"] = math.ceil(
        (statistics["goal"] - statistics["done_before_today"]) / (end_date - today).days
    )
    statistics["left_today"] = statistics["needed_day"] - statistics["done_today"]
    statistics["done_today_percent"] = round(
        statistics["done_today"] / statistics["needed_day"] * 100
    )

    return statistics

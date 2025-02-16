from datetime import date, timedelta
import math

from django.http import HttpResponse
from django.http import HttpRequest as HttpRequestBase
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models import Sum, Max, F
from django.db.models.functions import Coalesce

from django_htmx.middleware import HtmxDetails
from django_htmx.http import trigger_client_event

from pushuplog.models import PushupLogEntry
from pushuplog.forms import PushupLogForm
from users.models import User


# Hack for type-checking
class HttpRequest(HttpRequestBase):
    htmx: HtmxDetails


def index(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect("home")

    return render(request, "index.html")


@login_required
def home(request: HttpRequest) -> HttpResponse:
    context = {}

    form = PushupLogForm({"repetitions": get_latest_reps(request.user) or 10})
    statistics = get_statistics(request.user)

    context["form"] = form
    context["statistics"] = statistics
    return render(request, "home.html", context)


@login_required
def logentryform(request: HttpRequest, full_form=False) -> HttpResponse:
    form = PushupLogForm(request.POST, full_form=full_form)
    return render(request, "components/logform.html", {"form": form})


@login_required
def savelogentry(request: HttpRequest) -> HttpResponse:
    context = dict()
    full_form = False
    form = PushupLogForm(request.POST)
    if form.is_valid():
        kw = {
            "repetitions": form.cleaned_data["repetitions"],
            "user": request.user,
        }
        if form.cleaned_data["when"]:
            kw["when"] = form.cleaned_data["when"]
            full_form = True
        new_entry = PushupLogEntry.objects.create(**kw)
        context["new_entry"] = new_entry
        form = PushupLogForm(
            {"repetitions": get_latest_reps(request.user) or 10}, full_form=full_form
        )

    response = render(request, "components/logform.html", {"form": form})
    if form.is_valid():
        return trigger_client_event(response, "newLogentry")
    else:
        return response


@login_required
def dailyprogress(request: HttpRequest) -> HttpResponse:
    context = dict()
    stats = get_statistics(request.user)
    context["done"] = stats["done_today"]
    context["left"] = stats["left_today"]
    context["done_percent"] = stats["done_today_percent"]
    context["updated"] = True

    return render(request, "components/dailyprogresscard.html", context)


@login_required
def statistics(request: HttpRequest) -> HttpResponse:
    context = dict()
    context["statistics"] = get_statistics(request.user)
    context["updated"] = True

    return render(request, "components/statisticscard.html", context)


@login_required
def logs(request: HttpRequest) -> HttpResponse:
    pushup_log = (
        PushupLogEntry.objects.filter(user=request.user)
        .values(when_date=F("when__date"))
        .annotate(repetitions_sum=Sum("repetitions"))
        .order_by("-when_date")
    )

    context = {
        "pushup_log": pushup_log,
    }

    return render(request, "logs.html", context)


@login_required
def logsfordate(request: HttpRequest, year: int, month: int, day: int) -> HttpResponse:
    pushup_log = PushupLogEntry.objects.filter(
        user=request.user, when__date=date(year, month, day)
    )

    context = {"pushup_log": pushup_log}

    result = render(request, "components/dailylogtable.html", context)
    return result


@login_required
def editlogentry(request: HttpRequest, id: int) -> HttpResponse:
    entry = PushupLogEntry.objects.get(id=id)
    year, month, day = entry.when.date().year, entry.when.month, entry.when.day
    entry.delete()

    daily_stats = (
        PushupLogEntry.objects.filter(
            user=request.user, when__date=date(year, month, day)
        )
        .values(when_date=F("when__date"))
        .annotate(repetitions_sum=Sum("repetitions"))
    )[0]

    pushup_log = PushupLogEntry.objects.filter(
        user=request.user, when__date=date(year, month, day)
    )

    context = {
        "entry": daily_stats,
        "pushup_log": pushup_log,
        "expand": True,
    }

    return render(request, "components/dailylog.html", context)


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
    start_date = date(2025, 1, 1)
    end_date = date(2026, 1, 1)
    today = date.today()
    yesterday = date.today() - timedelta(days=1)

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
    statistics.update(
        PushupLogEntry.objects.filter(user=user)
        .values("when__date")
        .annotate(pushups=Sum("repetitions"))
        .aggregate(max_day=Max("pushups"))
    )
    statistics["needed_day"] = math.ceil(
        (statistics["goal"] - statistics["done_before_today"]) / (end_date - today).days
    )

    statistics["avg_day"] = round(
        statistics["done_before_today"] / (yesterday - start_date).days
    )
    statistics["left_today"] = statistics["needed_day"] - statistics["done_today"]
    statistics["done_today_percent"] = round(
        statistics["done_today"] / statistics["needed_day"] * 100
    )

    return statistics

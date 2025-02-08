from datetime import date, timedelta
import math

from django.http import HttpResponse
from django.http import HttpRequest as HttpRequestBase
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models import Sum, Max
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

    return render(request, "components/statisticscard.html", context)


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

"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path

from pages import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
    path("accounts/", include("allauth.urls")),
    path("", views.index, name="index"),
    path("home/", views.home, name="home"),
    path("logs/", views.logs, name="logs"),
    path("logs/<int:year>/<int:month>", views.logs, name="logsformonth"),
    path(
        "logs/<int:year>/<int:month>/<int:day>", views.logsfordate, name="logsfordate"
    ),
    path("logentryform/", views.logentryform, name="logentryform"),
    path(
        "logentryform/full/",
        views.logentryform,
        {"full_form": True},
        name="logentryform_full",
    ),
    path("savelogentry/", views.savelogentry, name="savelogentry"),
    path("editlogentry/<int:id>", views.editlogentry, name="editlogentry"),
    path("dailyprogress/", views.dailyprogress, name="dailyprogress"),
    path("statistics/", views.statistics, name="statistics"),
]

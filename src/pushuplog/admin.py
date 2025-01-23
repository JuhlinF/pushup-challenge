from django.contrib import admin
from pushuplog.models import PushupLogEntry


# Register your models here.
class PushupLogEntryAdmin(admin.ModelAdmin):
    list_display = ["user", "repetitions", "when", "updated_at", "created_at"]
    date_hierarchy = "when"
    list_filter = ["user"]


admin.site.register(PushupLogEntry, PushupLogEntryAdmin)

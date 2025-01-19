import csv
import pytz
from datetime import datetime

from django.core.management.base import BaseCommand, CommandError

from users.models import User
from pushuplog.models import PushupLogEntry


class Command(BaseCommand):
    help = "Import pushup log entries from the specified file to the specified user."

    def add_arguments(self, parser):
        parser.add_argument("user", help="The user to add push-up log entries to.")
        parser.add_argument(
            "file",
            help="CSV file with push-up log entries to import. ",
        )
        parser.add_argument(
            "--delete",
            "-d",
            action="store_true",
            help="Delete any existing log entries for the user.",
        )

    def handle(self, *args, **options):
        try:
            user = User.objects.get(email=options["user"])
        except User.DoesNotExist:
            raise CommandError(f'User "{options["user"]}" does not exist')

        try:
            csvfile = open(options["file"], newline="")
        except FileNotFoundError:
            raise CommandError(f'Unable to open file "{options["file"]}".')

        if options["delete"]:
            res = PushupLogEntry.objects.filter(user=user).delete()
            self.stdout.write(
                self.style.SUCCESS(f"Successfully deleted {res[0]} entries")
            )

        dialect = csv.Sniffer().sniff(csvfile.read(1024))
        csvfile.seek(0)
        logreader = csv.reader(csvfile, dialect)

        row_num = 0
        when = None
        for row in logreader:
            row_num += 1
            if len(row) == 2:  # If only two columns, "set" is assumed to be 1
                sets = 1
                repetitions = row[1]
            elif len(row) == 3:
                sets = row[1]
                repetitions = row[2]
            else:
                raise CommandError(
                    f"Incorrect number of fields in row {row_num}: {len(row)}"
                )

            if len(row[0]):  # If first column ("when") is empty, use previous value
                when = row[0]

                # Turn "when" into a datetime
                try:
                    when = datetime.fromisoformat(when)
                except ValueError:
                    raise CommandError(
                        f'Row {row_num}: incorrect date format: "{when}"'
                    )
                # If "when" is timezone naive, set it to UTC
                if when.tzinfo is None or when.tzinfo.utcoffset(when) is None:
                    when = when.replace(tzinfo=pytz.UTC)

            elif when is None:
                raise CommandError(
                    'The "when" column of the first row must not be empty'
                )

            PushupLogEntry.objects.create(
                user=user, when=when, sets=sets, repetitions=repetitions
            )

        self.stdout.write(
            self.style.SUCCESS(f"Successfully imported {row_num} entries")
        )

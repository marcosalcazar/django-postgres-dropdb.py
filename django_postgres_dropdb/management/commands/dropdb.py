from django.conf import settings
from django.core import management
from django.core.management.base import BaseCommand
import subprocess


"""
https://www.postgresql.org/docs/current/app-dropdb.html
"""


class Command(BaseCommand):
    help = 'drop postgres database'

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument('alias',nargs='?', default="default")
        parser.add_argument("ignore-errors", nargs="?", default="default")
        parser.add_argument("-i", "--ignore-errors", dest="ignore_errors", action="store_true", default=False)

    def handle(self, *args, **options):
        alias = options.get('alias')
        ignore_errors = options.get('ignore_errors')

        db_settings = settings.DATABASES[alias]
        args = ['dropdb']
        if 'USER' in db_settings:
            args+=["-U",db_settings['USER']]
        if 'HOST' in db_settings:
            args+=["-h",db_settings['HOST']]
        if 'PORT' in db_settings:
            args+=["-p",str(db_settings['PORT'])]
        args.append(db_settings['NAME'])
        if not ignore_errors:
            subprocess.check_call(args)
        else:
            subprocess.call(args)

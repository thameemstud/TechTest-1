#from django.contrib.auth.management.commands import createsuperuser
from django.core.management.base import BaseCommand, CommandError
from django.core.management import CommandError
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Crate a superuser, and allow password to be provided'

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument(
            '--password', dest='password', default=None,
            help='Specifies the password for the superuser.',
        )
        parser.add_argument(
            '--preserve', dest='preserve', default=False, action='store_true',
            help='Exit normally if the user already exists.',
        )

    def handle(self, *args, **options):
        password = 'admin1234'
        username = 'admin'
        email = 'admin@example.com'

        if password and not username:
            raise CommandError("--username is required if specifying --password")

        if username:
            exists = User.objects.filter(username=username).exists()
            if exists:
                self.stdout.write("User exists, exiting normally due to --preserve")
                return
                
        user = User.objects.create_user(username, email, password)
        user.save()

        

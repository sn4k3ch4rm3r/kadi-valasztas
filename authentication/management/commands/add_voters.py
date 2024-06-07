import sys
from django.core.management import BaseCommand
from authentication.models import User


class Command(BaseCommand):
    help = 'Create users from a file containing email addresses'

    def add_arguments(self, parser):
        parser.add_argument(
            'file_path', type=str, help='The file path of the email addresses or "-" for stdin')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']

        if file_path == '-':
            emails = sys.stdin.readlines()
        else:
            try:
                with open(file_path, 'r') as file:
                    emails = file.readlines()
            except FileNotFoundError:
                self.stdout.write(self.style.ERROR(
                    f'File not found: {file_path}'))
                return

        for email in emails:
            email = email.strip()
            self.stdout.write(email)
            if email != "":
                user, created = User.objects.get_or_create(email=email)
                user.can_vote = True
                user.save()
                if not created:
                    self.stdout.write(f"{email} duplicated.")

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from main.models import Admin

class Command(BaseCommand):
    help = 'Create an admin user with a hashed password'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username of the admin user')
        parser.add_argument('password', type=str, help='Password of the admin user')
        parser.add_argument('email', type=str, help='Email of the admin user')

    def handle(self, *args, **kwargs):
        username = kwargs['username']
        password = kwargs['password']
        email = kwargs['email']
        
        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f'User "{username}" already exists.'))
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            Admin.objects.create(user=user)
            self.stdout.write(self.style.SUCCESS(f'Successfully created admin user "{username}"'))
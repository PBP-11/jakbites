
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from main.models import Client

class Command(BaseCommand):
    help = 'Create a client user with a hashed password'

    def handle(self, *args, **kwargs):
        username = "client"
        password = "client123"
        email = "client@gmail.com"
        
        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f'User "{username}" already exists.'))
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            Client.objects.create(user=user)
            self.stdout.write(self.style.SUCCESS(f'Successfully created client user "{username}"'))
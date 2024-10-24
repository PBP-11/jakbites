from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from main.models import Admin

class Command(BaseCommand):
    help = 'Create an admin user with a hashed password'

    def handle(self, *args, **kwargs):
        username = 'admin'
        password = 'admin123'
        email = 'admin@example.com'
        
        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f'User "{username}" already exists.'))
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            Admin.objects.create(user=user)
            self.stdout.write(self.style.SUCCESS(f'Successfully created admin user "{username}"'))
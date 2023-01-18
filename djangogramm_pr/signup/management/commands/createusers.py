from django.core.management.base import BaseCommand
from faker import Faker

from signup.models import User

USERS_COUNT = 10
faker = Faker('en_US')


class Command(BaseCommand):
    help = 'Populates database with fake users'

    def add_arguments(self, parser):
        parser.add_argument('--users', '-u', type=int)

    def handle(self, *args, **options):
        for _ in range(options['users'] if options['users'] else USERS_COUNT):
            profile_data = faker.simple_profile()

            user_to_create = User(username=profile_data['username'], email=profile_data['mail'])
            password = User.objects.make_random_password()
            user_to_create.set_password(password)
            user_to_create.is_active = True
            user_to_create.save()

        self.stdout.write(f"Fake users created successfully \nUsers in database: {User.objects.count()}")


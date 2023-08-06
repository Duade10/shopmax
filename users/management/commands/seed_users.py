import random
from django.core.management.base import BaseCommand
from django_seed import Seed
from users import models as user_models
from stations_132.models import Station_132
from stations_330.models import Station_330


class Command(BaseCommand):

    help = "This command creates many users"

    def add_arguments(self, parser):
        parser.add_argument("--number", default=1, help="How many users do you want to create?")

    def handle(self, *args, **options):
        number = options.get("number")
        number = int(number)
        seeder = Seed.seeder()
        seeder.add_entity(user_models.User, number, {"is_staff": False, "is_superuser": False})
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number}  users created! "))

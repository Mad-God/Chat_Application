import random
from django.core.management.base import BaseCommand
from faker import Faker, providers

# import faker.providers


from base.models import User
from chat.models import ChatGroup, Member

USERS = list(User.objects.all())


class UsersProvider(providers.BaseProvider):
    def user(self):
        return self.random_element(USERS)


class Command(BaseCommand):
    help = "Add ChatGroups fake data to db"

    def add_arguments(self, parser):
        parser.add_argument("--num", nargs="+", type=int)

    def handle(self, *args, **kwargs):
        check_groups = ChatGroup.objects.all().count()
        self.stdout.write(
            self.style.SUCCESS(f"Number of ChatGroups (before): {check_groups}")
        )

        fake = Faker(["en_IN"])
        fake.add_provider(UsersProvider)
        print(kwargs)
        for _ in range(kwargs["num"][0] if "num" in kwargs else 5):
            # for _ in range(5):
            g_name = fake.unique.sentence()
            user = fake.user()
            x = ChatGroup.objects.create(name=g_name[:13])
            x.admin.add(user.id)
            Member.objects.create(group=x, user=user, accepted=True)
            admin = User.objects.get(id=1)
            if user.id != 1:
                x.admin.add(1)
                Member.objects.create(group=x, user=admin, accepted=True)

        check_group = ChatGroup.objects.all().count()
        self.stdout.write(
            self.style.SUCCESS(f"Number of Chat groups (after): {check_group}")
        )

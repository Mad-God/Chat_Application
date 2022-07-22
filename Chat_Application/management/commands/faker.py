# from faker import Faker
# from faker.providers import DynamicProvider
# import factory


# # custom
# from base.models import User
# from ....chat.models import ChatGroup

# users = DynamicProvider(
#      provider_name="user",
#      elements=list(User.objects.all()),
# )

# fakeGroups = Faker()

# # add User provider field to faker
# fakeGroups.add_provider(users)


import random

import faker.providers
from django.core.management.base import BaseCommand
from faker import Faker


from base.models import User
from chat.models import ChatGroup

USERS = list(User.objects.all())


class UsersProvider(faker.providers.BaseProvider):
    def user(self):
        return self.random_element(USERS)


class AddFakeChatGroups(BaseCommand):
    help = "Add ChatGroups fake data to db"

    def handle(self, *args, **kwargs):
        check_groups = ChatGroup.objects.all().count()
        self.stdout.write(
            self.style.SUCCESS(f"Number of categories(before): {check_groups}")
        )

        fake = Faker(["en_IN"])
        fake.add_provider(UsersProvider)

        for _ in range(5):
            g_name = fake.unique.text(nb_words=2)
            user = fake.user()
            ChatGroup.objects.create(name=g_name, admin=user)

        # for _ in range(15):
        #     e = fake.unique.ecommerce_products()
        #     ProductType.objects.create(name=e)

        # for _ in range(15):
        #     pt = fake.text(max_nb_chars=30)
        #     cid = random.randint(1, 15)
        #     ptid = random.randint(1, 15)
        #     Product.objects.create(
        #         product_type_id=ptid,
        #         category_id=cid,
        #         title=pt,
        #         description=fake.text(max_nb_chars=100),
        #         regular_price=(round(random.uniform(50.99, 99.99), 2)),
        #         discount_price=(round(random.uniform(10.99, 49.99), 2)),
        #     )

        # for i in range(1, 16):
        #     ProductImage.objects.create(product_id=i, alt_text=fake.text(max_nb_chars=30), is_feature=True)

        check_group = ChatGroup.objects.all().count()
        self.stdout.write(
            self.style.SUCCESS(f"Number of categories(after): {check_group}")
        )




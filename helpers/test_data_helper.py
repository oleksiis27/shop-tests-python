import random
from faker import Faker

fake = Faker()


class TestDataHelper:
    @staticmethod
    def random_email() -> str:
        return fake.email()

    @staticmethod
    def random_password() -> str:
        return fake.password(length=random.randint(8, 20))

    @staticmethod
    def random_name() -> str:
        return fake.name()

    @staticmethod
    def random_product(category_id: int = 1) -> dict:
        name = f"{fake.word().capitalize()} {fake.word().capitalize()}"
        slug = name.lower().replace(" ", "-")
        return {
            "name": name,
            "description": fake.sentence(nb_words=10),
            "price": round(random.uniform(10, 1000), 2),
            "stock": random.randint(1, 100),
            "category_id": category_id,
            "image_url": f"https://example.com/images/{slug}.jpg",
        }

    @staticmethod
    def random_product_high_stock(category_id: int = 1) -> dict:
        product = TestDataHelper.random_product(category_id)
        product["stock"] = 9999
        return product

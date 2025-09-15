from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.db import transaction
from django.conf import settings
from pathlib import Path
from io import BytesIO
from PIL import Image
import random

from main import models

COLORS = ["red", "green", "blue", "orange", "purple", "gray"]


def generate_image(color: str, size=(600, 400)):
    image = Image.new("RGB", size, color=color)
    buf = BytesIO()
    image.save(buf, format="JPEG")
    return ContentFile(buf.getvalue(), name=f"{color}.jpg")


class Command(BaseCommand):
    help = "Seed demo data for development"

    @transaction.atomic
    def handle(self, *args, **options):
        Path(settings.MEDIA_ROOT).mkdir(parents=True, exist_ok=True)

        models.ProductImage.objects.all().delete()
        models.Product.objects.all().delete()
        models.Category.objects.all().delete()
        models.Advantage.objects.all().delete()
        models.Metric.objects.all().delete()
        models.TeamMember.objects.all().delete()
        models.Value.objects.all().delete()
        models.CompanyInfo.objects.all().delete()
        models.CarouselItem.objects.all().delete()

        categories = []
        for i in range(1, 6):
            cat = models.Category.objects.create(name=f"Category {i}")
            categories.append(cat)

        for i in range(1, 41):
            cat = random.choice(categories)
            product = models.Product.objects.create(
                name=f"Product {i}",
                description="Demo product",
                price=random.randint(10, 1000),
                category=cat,
            )
            for n in range(1, 4):
                color = random.choice(COLORS)
                img = generate_image(color)
                models.ProductImage.objects.create(
                    product=product,
                    image=img,
                    alt_text=f"Image {n}",
                    ordering=n,
                    is_primary=(n == 1),
                )

        for i in range(1, 4):
            img = generate_image(random.choice(COLORS))
            models.CarouselItem.objects.create(title=f"Slide {i}", image=img, ordering=i)

        for i in range(1, 4):
            models.Advantage.objects.create(title=f"Advantage {i}", description="Desc", ordering=i)

        for i in range(1, 5):
            models.Metric.objects.create(name=f"Metric {i}", value=str(i * 10), suffix="units", ordering=i)

        for i in range(1, 5):
            img = generate_image(random.choice(COLORS), size=(300, 300))
            models.TeamMember.objects.create(full_name=f"Member {i}", role="Role", photo=img, ordering=i)

        for i in range(1, 5):
            models.Value.objects.create(title=f"Value {i}", description="Desc", ordering=i)

        models.CompanyInfo.objects.create(mission_text="Our mission", about_text="About us")

        self.stdout.write(self.style.SUCCESS("Demo data created"))

from django.core.management.base import BaseCommand
from django.utils import timezone
from api.models import Product, ProductImage, Material, ContactUs, Inquiry, InquiryItems
from faker import Faker
import random
from datetime import timedelta
import uuid

fake = Faker()

class Command(BaseCommand):
    help = 'Generates fake data for testing'

    def handle(self, *args, **kwargs):
        self.stdout.write('Generating fake data...')

        # Create Materials
        materials = []
        material_types = ['Cotton', 'Polyester', 'Wool', 'Silk', 'Linen', 'Leather', 'Denim', 'Nylon']
        for material in material_types:
            material_obj = Material.objects.create(material=material)
            materials.append(material_obj)
        self.stdout.write(f'Created {len(materials)} materials')

        # Create Product Images
        product_images = []
        for _ in range(20):
            image = ProductImage.objects.create(
                image_url=f"product_images/fake_image_{uuid.uuid4()}.jpg"
            )
            product_images.append(image)
        self.stdout.write(f'Created {len(product_images)} product images')

        # Create Products
        products = []
        categories = ['Shirts', 'Pants', 'Dresses', 'Jackets', 'Accessories']
        main_categories = ['Men', 'Women', 'Kids', 'Unisex']
        sample_types = ['Production', 'Development', 'Prototype']

        for _ in range(900):
            date = timezone.now() - timedelta(days=random.randint(1, 365))
            product = Product.objects.create(
                name=fake.catch_phrase(),
                style_number=f"STY-{random.randint(1000, 9999)}",
                date=date,
                description=fake.text(),
                sample_type=random.choice(sample_types),
                category=random.choice(categories),
                main_category=random.choice(main_categories),
                price=random.uniform(10.0, 500.0),
                image=f"product_images/main_image_{uuid.uuid4()}.jpg"
            )
            # Add random materials and images
            product.materials.add(*random.sample(materials, k=random.randint(1, 3)))
            product.images.add(*random.sample(product_images, k=random.randint(1, 5)))
            products.append(product)
        self.stdout.write(f'Created {len(products)} products')

        # Create Contact Us entries
        for _ in range(100):
            ContactUs.objects.create(
                name=fake.name(),
                email=fake.email(),
                subject=fake.sentence(),
                message=fake.text(),
                is_read=random.choice([True, False]),
                created_at=timezone.now() - timedelta(days=random.randint(1, 30))
            )
        self.stdout.write('Created 100 contact us entries')

        # Create Inquiry Items and Inquiries
        inquiries = []
        for _ in range(100):
            # Create Inquiry
            inquiry = Inquiry.objects.create(
                name=fake.name(),
                email=fake.email(),
                subject=fake.sentence(),
                message=fake.text(),
                is_read=random.choice([True, False]),
                created_at=timezone.now() - timedelta(days=random.randint(1, 30))
            )
            
            # Create and add random inquiry items
            num_items = random.randint(1, 5)
            for product in random.sample(products, k=num_items):
                item = InquiryItems.objects.create(product=product)
                inquiry.items.add(item)
            
            inquiries.append(inquiry)
        
        self.stdout.write('Created 100 inquiries with items')
        self.stdout.write(self.style.SUCCESS('Successfully generated fake data')) 
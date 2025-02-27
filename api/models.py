from django.db import models
from uuid import uuid4
# Create your models here.
class ProductImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True)
    image_url = models.FileField(upload_to='product_images/')

    def __str__(self):
        return self.image_url.name


class Material(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True)
    material = models.CharField(max_length=50)

    def __str__(self):
        return self.material


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True)
    name = models.CharField(max_length=200)
    style_number = models.CharField(max_length=50)
    date = models.DateField()
    description = models.TextField()
    sample_type = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    main_category = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.FileField(upload_to='product_images/')
    images = models.ManyToManyField(ProductImage, related_name='product_images')
    materials = models.ManyToManyField(Material, related_name='product_materials')

    def __str__(self):
        return self.name



class BaseContact(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ContactUs(BaseContact):

    
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.email} - {self.subject}"
    class Meta:
        verbose_name = 'Contact Us'
        verbose_name_plural = 'Contact Us'

class InquiryItems(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.name}"
    
    class Meta:
        verbose_name = 'Inquiry Item'
        verbose_name_plural = 'Inquiry Items'
    
class Inquiry(BaseContact):

    items = models.ManyToManyField(InquiryItems, blank=True)
    is_read = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.name} - {self.email} - {self.subject}"
    
    class Meta:
        verbose_name = 'Inquiry'
        verbose_name_plural = 'Inquiries'




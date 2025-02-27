from django.contrib import admin

# Register your models here.
from .models import Product, ProductImage, Material, ContactUs, Inquiry, InquiryItems

class InquiryItemsInline(admin.TabularInline):
    model = Inquiry.items.through
    extra = 1

@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'created_at', 'is_read']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'subject']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [InquiryItemsInline]
    exclude = ('items',)  # Hide the items field since we're using inline

@admin.register(InquiryItems)
class InquiryItemsAdmin(admin.ModelAdmin):
    list_display = ['id', 'product']
    search_fields = ['product__name']

admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Material)
admin.site.register(ContactUs)



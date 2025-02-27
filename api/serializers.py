from rest_framework import serializers
from .models import Product, ProductImage, Material, ContactUs, Inquiry, InquiryItems

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image_url']

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ['id', 'material']


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'name', 'style_number', 'date', 'category', 'main_category', 'price', 'image']



class ProductDetailSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True)
    materials = MaterialSerializer(many=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'style_number', 'date', 'description', 'sample_type', 'category', 'main_category', 'price', 'image', 'images', 'materials']


class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = ['id', 'name', 'email', 'subject', 'message']



class InquiryItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = InquiryItems
        fields = ['id', 'product']



class InquirySerializer(serializers.ModelSerializer):
    items = InquiryItemsSerializer(many=True, required=False)
    
    class Meta:
        model = Inquiry
        fields = ['id', 'name', 'email', 'subject', 'message', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        inquiry = Inquiry.objects.create(**validated_data)
        
        # Create and add items
        if items_data:
            for item_data in items_data:
                item = InquiryItems.objects.create(**item_data)
                inquiry.items.add(item)
        
        return inquiry

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['items'] = InquiryItemsSerializer(instance.items.all(), many=True).data
        return representation





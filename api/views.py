from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django.core.exceptions import ValidationError
from django.db.models import Prefetch
from django.conf import settings
from .models import Product, ProductImage, Material, ContactUs, Inquiry
from .serializers import ProductSerializer, ProductDetailSerializer, ContactUsSerializer, InquirySerializer 
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .services.email_service import EmailService

class ProductList(APIView):
    '''
    Get all products with pagination
    used select_related to reduce the number of queries
    used cache_page to cache the response
    '''
    @method_decorator(cache_page(60 * 15))  # Cache for 15 minutes
    @method_decorator(vary_on_cookie)
    def get(self, request):
        try:
            # Add pagination
            page = int(request.GET.get('page', 1))
            page_size = int(request.GET.get('page_size', settings.DEFAULT_PAGE_SIZE))
            
            # Validate pagination parameters
            if page < 1 or page_size < 1:
                raise ValidationError("Invalid pagination parameters")
            
            # Calculate offset
            offset = (page - 1) * page_size
            
            # Only select the fields we need for the list view with pagination
            products = Product.objects.only(
                'id', 'name', 'style_number', 'date', 
                'category', 'main_category', 'price', 'image'
            ).order_by('-date')[offset:offset + page_size]
            
            # Get total count for pagination
            total_count = Product.objects.count()
            
            serializer = ProductSerializer(products, many=True)
            return Response(
                {   
                    'status': 'success',
                    'message': 'Products fetched successfully',
                    'products': serializer.data,
                    'pagination': {
                        'current_page': page,
                        'page_size': page_size,
                        'total_items': total_count,
                        'total_pages': (total_count + page_size - 1) // page_size
                    }
                },
                status=status.HTTP_200_OK
            )
        except ValidationError as e:
            return Response(
                {
                    'status': 'error',
                    'message': str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {
                    'status': 'error',
                    'message': 'An error occurred while fetching products'
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ProductDetail(APIView):
    '''
    Get selected id products
    used select_related and prefetch_related to reduce the number of queries
    used cache_page to cache the response
    '''
    @method_decorator(cache_page(60 * 15))  # Cache for 15 minutes
    @method_decorator(vary_on_cookie)
    def get(self, request, pk):
        try:
            # Optimize query with specific prefetch related
            product = get_object_or_404(
                Product.objects.prefetch_related(
                    Prefetch(
                        'images',
                        queryset=ProductImage.objects.only('id', 'image_url')
                    ),
                    Prefetch(
                        'materials',
                        queryset=Material.objects.only('id', 'material')
                    )
                ).select_related(),
                pk=pk
            )
            
            serializer = ProductDetailSerializer(product)
            return Response(
                {   
                    'status': 'success',
                    'message': 'Product details fetched successfully',
                    'product': serializer.data
                },
                status=status.HTTP_200_OK
            )
        except Product.DoesNotExist:
            return Response(
                {
                    'status': 'error',
                    'message': f'Product not found with id: {pk}'
                },
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {
                    'status': 'error',
                    'message': 'An error occurred while fetching product details'
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ContactUsView(APIView):
    """
    API view to handle contact form submissions
    """
    def post(self, request):
        serializer = ContactUsSerializer(data=request.data)
        if serializer.is_valid():
            contact = serializer.save()
            
            # Send email using the service
            email_sent = EmailService.send_contact_email(contact)
            
            response_data = {
                'status': 'success',
                'message': 'Contact form submitted successfully',
                'data': serializer.data
            }
            
            if not email_sent:
                response_data['warning'] = 'Form submitted but notification email failed'
            
            return Response(response_data, status=status.HTTP_201_CREATED)
            
        return Response(
            {
                'status': 'error', 
                'message': 'Invalid data provided',
                'errors': serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )

class InquiryView(APIView):
    """
    API view to handle inquiry form submissions
    """
    def post(self, request):
        serializer = InquirySerializer(data=request.data)
        if serializer.is_valid():
            inquiry = serializer.save()
            
            # Send email using the service
            email_sent = EmailService.send_inquiry_email(inquiry)
            
            response_data = {
                'status': 'success',
                'message': 'Inquiry submitted successfully',
                'data': serializer.data
            }
            
            if not email_sent:
                response_data['warning'] = 'Inquiry submitted but notification email failed'
            
            return Response(response_data, status=status.HTTP_201_CREATED)
            
        return Response(
            {
                'status': 'error',
                'message': 'Invalid data provided', 
                'errors': serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )

from django.contrib import admin
from django.urls import path
from .views import ProductList, ProductDetail, ContactUsView, InquiryView




urlpatterns = [
    path('products/', ProductList.as_view(), name='product-list'),
    path('products/<uuid:pk>/', ProductDetail.as_view(), name='product-detail'),
    path('contact-us/', ContactUsView.as_view(), name='contact-us'),
    path('inquiry/', InquiryView.as_view(), name='inquiry'),
] 

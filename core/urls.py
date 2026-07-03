from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("services/", views.services, name="services"),
    path("our-products/", views.our_products, name="our_products"),
    path("our-products/<slug:slug>/", views.product_detail, name="product_detail"),
    path("solutions/", views.solutions, name="solutions"),
    path("careers/", views.careers, name="careers"),
    path("contact/", views.contact, name="contact"),
    path("services/<slug:slug>/", views.service_detail, name="service_detail"),
]
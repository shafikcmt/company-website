from django.urls import path
from hapl import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("customers/", views.customers, name="customers"),
    path("contact/", views.contact, name="contact"),
    path("activities/", views.activities, name="activities"),
    path("career/", views.career, name="career"),
    path("career/<int:position_id>/apply/", views.career_apply, name="career_apply"),
    path("products/", views.products, name="products"),
    path("compliance/", views.complience, name="complience"),
    path("sustainability/", views.sustainability, name="sustainability"),
    path("gallery/", views.gallery, name="gallery"),
]

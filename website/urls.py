from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('predict-crop/', views.predict_crop, name='predict_crop'),
    path('features/', views.features, name='features'),
    path('gallery/', views.gallery, name='gallery'),
    path('facts/', views.facts, name='facts'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
] 
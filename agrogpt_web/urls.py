from django.contrib import admin
from django.urls import path
from website import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('facts/', views.facts, name='facts'),
    path('gallery/', views.gallery, name='gallery'),
    path('features/', views.features, name='features'),
    path('predict/', views.predict_crop, name='predict_crop'),
    path('send-contact-email/', views.send_contact_email, name='send_contact_email'),
] 
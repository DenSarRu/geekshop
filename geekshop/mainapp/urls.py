from django.urls import path
from .views import products, category

app_name = 'mainapp'

urlpatterns = [
    path('', products, name='main'),
    path('<int:pk>/', products, name='category'),
]

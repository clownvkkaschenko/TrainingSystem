from django.urls import path

from .views import buy_product, products, products_stats, student_lessons

app_name = 'api'


urlpatterns = [
    path('products/', products),
    path('products_stats/', products_stats),
    path('student/<int:student_id>/product/<int:product_id>/buy/', buy_product),
    path('student/<int:student_id>/product/<int:product_id>/', student_lessons),
]

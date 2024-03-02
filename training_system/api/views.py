from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import decorators, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .helpers import add_student_in_new_group
from .models import Product, Student
from .serializers import (LessonSerializer, ProductSerializer,
                          ProductStatsSerializer)


@decorators.api_view(['GET'])
def products(request):
    """Выводим продукты, доступные для покупки."""

    current_time = timezone.now()
    products = Product.objects.filter(start_date__gt=current_time).order_by('id')

    paginator = PageNumberPagination()
    paginated_products = paginator.paginate_queryset(products, request)
    serializer = ProductSerializer(paginated_products, many=True)

    return paginator.get_paginated_response(serializer.data)


@decorators.api_view(['POST'])
def buy_product(request, student_id: int, product_id: int):
    """Покупаем продукт и добавляем студента в группу."""

    current_time = timezone.now()
    products = Product.objects.filter(start_date__gt=current_time).order_by('id')

    if product_id not in [product.id for product in products]:
        return Response(
                {'message': 'Даный продукт уже нельзя купить.'},
                status=status.HTTP_400_BAD_REQUEST
        )

    product = get_object_or_404(Product, id=product_id)
    student = get_object_or_404(Student, id=student_id)

    if student.has_access_to_product(product_id=product_id):
        return Response(
                {'message': 'У вас уже есть доступ к данному продукту.'},
                status=status.HTTP_400_BAD_REQUEST
        )

    groups = product.training_groups_related.all()
    max_students = product.max_number_of_students

    if groups.count() == 0:
        add_student_in_new_group(product, student)

    for group in groups:
        if group.students.count() < max_students:
            group.students.add(student)
            product.students.add(student)
            return Response({'message': 'Продукт куплен.'}, status.HTTP_200_OK)
    else:
        add_student_in_new_group(product, student)


@decorators.api_view(['GET'])
def student_lessons(request, student_id: int, product_id: int):
    """Выводим список уроков, по конкретному продукту."""

    student = get_object_or_404(Student, id=student_id)
    if not student.has_access_to_product(product_id=product_id):
        return Response(
            {'message': 'У вас нет доступа к этому уроку.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    product = get_object_or_404(Product, id=product_id)
    lessons = product.lessons.all().order_by('id')

    paginator = PageNumberPagination()
    paginated_lessons = paginator.paginate_queryset(lessons, request)
    serializer = LessonSerializer(paginated_lessons, many=True)

    return paginator.get_paginated_response(serializer.data)


@decorators.api_view(['GET'])
def products_stats(request):
    """Выводим статистику по всем продуктам."""

    products = Product.objects.all().order_by('id')

    paginator = PageNumberPagination()
    paginated_products = paginator.paginate_queryset(products, request)
    serializer = ProductStatsSerializer(paginated_products, many=True)

    return paginator.get_paginated_response(serializer.data)

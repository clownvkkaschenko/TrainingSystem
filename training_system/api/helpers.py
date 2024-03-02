from rest_framework import status
from rest_framework.response import Response

from .models import TrainingGroup


def add_student_in_new_group(product, student):
    """Создаём новую группу и добавляем в неё студента, купившего доступ к продукту."""

    new_group_name = f"«{product.name}» группа № {product.training_groups_related.count() + 1}"
    new_group = TrainingGroup.objects.create(product=product, name=new_group_name)
    new_group.students.add(student)
    product.students.add(student)
    return Response({'message': 'Продукт куплен.'}, status.HTTP_200_OK)

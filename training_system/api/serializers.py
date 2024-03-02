from pytz import timezone as pytz_timezone
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import Lesson, Product, Student, Teacher, TrainingGroup


class LessonSerializer(ModelSerializer):
    """Сериализатор для информации об уроках."""

    product_name = serializers.CharField(source='product.name', read_only=True)
    lesson_name = serializers.CharField(source='name', read_only=True)

    class Meta:
        model = Lesson
        fields = ('product_name', 'lesson_name', 'link_to_video')


class TeacherSerializer(ModelSerializer):
    """Сериализатор для информации о преподователях."""

    class Meta:
        model = Teacher
        fields = ('first_name', 'last_name', 'age')


class ProductSerializer(ModelSerializer):
    """Сериализатор для информации о продуктах."""

    teacher = TeacherSerializer(read_only=True)
    cnt_lessons = SerializerMethodField()
    start_date_tz = SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'name', 'start_date_tz', 'price', 'cnt_lessons', 'teacher',
            'min_number_of_students', 'max_number_of_students',
        )

    def get_cnt_lessons(self, obj):
        """Получаем количество уроков, для каждого продукта."""

        return obj.lessons.count()

    def get_start_date_tz(self, obj):
        """Добавляем часовой пояс к полю start_date."""

        desired_timezone = pytz_timezone('Europe/Moscow')
        start_date_with_timezone = obj.start_date.astimezone(desired_timezone)
        return start_date_with_timezone.strftime('%d.%m.%Y %H:%M %Z')


class ProductStatsSerializer(ModelSerializer):
    """Сериализатор для статистики о продуктах."""

    product_purchase_percentage = SerializerMethodField()
    cnt_students = SerializerMethodField()
    group_occupancy_percentage = SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'id', 'name', 'cnt_students', 'group_occupancy_percentage',
            'product_purchase_percentage',
        )

    def get_cnt_students(self, obj):
        """Считаем количество учеников занимающихся на продукте."""

        return Student.objects.filter(products__id=obj.id).count()

    def get_group_occupancy_percentage(self, obj):
        """Считаем на сколько процентов заполнены группы."""

        total_students = Student.objects.filter(products__id=obj.id).count()
        total_groups = TrainingGroup.objects.filter(product=obj).count()
        average = total_students/total_groups if total_groups else 0

        max_number_of_students = obj.max_number_of_students

        return f'{round((average/max_number_of_students)*100, 2)} %'

    def get_product_purchase_percentage(self, obj):
        """Считаем процент приобретения продукта."""

        all_students: int = Student.objects.all().count()
        total_purchased = Student.objects.filter(products__id=obj.id).count()

        return f'{round((total_purchased/all_students)*100, 2)} %' if all_students else 0

from django.contrib import admin

from .models import Lesson, Product, Student, Teacher, TrainingGroup


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    """Класс для работы с преподавателями в админке."""

    list_display = ('id', 'first_name', 'last_name', 'email', 'age',)
    search_fields = ('last_name',)
    list_filter = ('products',)
    ordering = ('-id',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Класс для работы с продуктами в админке."""

    list_display = ('id', 'teacher', 'name', 'start_date',)
    fields = (
        'teacher', 'name', 'start_date', 'price',
        'min_number_of_students', 'max_number_of_students'
    )
    search_fields = ('name',)
    ordering = ('-id',)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    """Класс для работы с уроками в админке."""

    list_display = ('id', 'product', 'name',)
    fields = ('product', 'name', 'link_to_video')
    search_fields = ('name',)
    list_filter = ('product',)
    ordering = ('-id',)


@admin.register(TrainingGroup)
class TrainingGroupAdmin(admin.ModelAdmin):
    """Класс для работы с группами в админке."""

    list_display = ('id', 'product', 'name',)
    search_fields = ('name',)
    list_filter = ('product',)
    ordering = ('-id',)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    """Класс для работы со студентами в админке."""

    list_display = ('id', 'first_name', 'last_name', 'email', 'age',)
    search_fields = ('last_name', 'training_groups__name')
    list_filter = ('products',)
    filter_horizontal = ('training_groups', 'products')
    ordering = ('-id',)

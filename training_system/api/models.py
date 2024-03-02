from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models


class CustomBaseUser(models.Model):
    """Общая модель для преподавателей и студентов."""

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=40)
    email = models.EmailField(max_length=254, unique=True)
    age = models.PositiveSmallIntegerField(validators=[MinValueValidator(16)])

    class Meta:
        abstract = True


class Teacher(CustomBaseUser):
    """Модель для преподавателей/авторов курсов обучения.

    Поля модели:
      - first_name: Имя преподавателя.
      - last_name: Фамилия преподавателя.
      - email: Эл.почта преподавателя.
      - age: Возраст преподавателя.
    """

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Product(models.Model):
    """Модель для курсов обучения.

    Поля модели:
      - teacher(1:М с моделью «Teacher»): Преподаватель/автор продукта.
      - name: Название продукта.
      - start_date: Дата и время старта обучения.
      - price: Цена.
      - min_number_of_students: Минимальное количество студентов в группе
                                (задаётся внутри продукта).
      - max_number_of_students: Максимальное количество студентов в группе
                                (задаётся внутри продукта).
    """

    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=40, unique=True)
    start_date = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    min_number_of_students = models.PositiveIntegerField(default=1)
    max_number_of_students = models.PositiveIntegerField()

    def __str__(self):
        return self.name

    def clean(self):
        super().clean()
        if self.max_number_of_students < self.min_number_of_students:
            raise ValidationError('Максимальное количество студентов в группе не может '
                                  'быть меньше минимального.')


class Lesson(models.Model):
    """Модель для уроков.

    Поля модели:
      - product(1:М с моделью «Product»): Продукт(родитель) урока.
      - name: Название урока.
      - link_to_video: Ссылка на видео.
    """

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='lessons')
    name = models.CharField(max_length=60)
    link_to_video = models.URLField()

    class Meta:
        unique_together = ['product', 'name']

    def __str__(self):
        return self.name


class TrainingGroup(models.Model):
    """Модель для групп.

    Поля модели:
      - product(1:М с моделью «Product»): Продукт(родитель) группы.
      - name: Название группы.
    """

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='training_groups_related'
    )
    name = models.CharField(max_length=60, unique=True)

    def __str__(self):
        return self.name


class Student(CustomBaseUser):
    """Модель для студентов/клиентов.

    Поля модели:
      - products(M2M с моделью «Product»): Продукты студента.
      - training_groups(M2M с моделью «TrainingGroup»): Группы студента.
      - first_name: Имя студента.
      - last_name: Фамилия студента.
      - email: Эл.почта студента.
      - age: Возраст студента.
    """

    products = models.ManyToManyField(Product, related_name='students', blank=True)
    training_groups = models.ManyToManyField(
        TrainingGroup, related_name='students', blank=True
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def has_access_to_product(self, product_id: int) -> bool:
        """Проверяем что у студента/клиента есть доступ к продукту.

        Args:
            - product_id (int): ID продукта.
        """

        return self.products.filter(id=product_id).exists()

from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class User(models.Model):
    """
    Описание:
    ---------
    Класс User представляет собой базовую модель сотрудника компании.

    Поля:
    -----
    first_name - имя
    second_name - фамилия
    patronymic - отчество
    age - возраст
    departament - отдел компании
    post - должность
    email - адрес электронной почты

    Дополнительные методы:
    ----------------------
    validation - метод проверки полей email и age.
    __str__ - переопределяет метод, возвращающий адрес электронной почты
              вместо идентификатора по умолчанию.
    """

    first_name = models.CharField(max_length=16,
                                  null=False,
                                  blank=False,
                                  verbose_name='имя')
    second_name = models.CharField(max_length=35,
                                   null=False,
                                   blank=False,
                                   verbose_name='фамилия')
    patronymic = models.CharField(max_length=35,
                                  null=False,
                                  blank=False,
                                  verbose_name='отчество')
    age = models.IntegerField(verbose_name='возраст',
                              validators=(
                                  MinValueValidator(
                                      18,
                                      message='Минимальный возраст 18 лет!'
                                      ),
                                  MaxValueValidator(
                                      75,
                                      message='Максимальный возраст 75 лет!'
                                      )))
    departament = models.CharField(max_length=50,
                                   null=False,
                                   blank=False,
                                   verbose_name='отдел')
    post = models.CharField(max_length=50,
                            null=False,
                            blank=False,
                            verbose_name='должность')
    email = models.EmailField(blank=False,
                              null=False)

    class Meta:
        ordering = ['email']

    def validation(self):
        """Метод проверки полей email и age."""
        if not self.email.endswith('@example.com'):
            raise ValidationError({'email': 'Invalid email address'})

    def __str__(self) -> str:
        return self.email


class Link(models.Model):
    """
    Описание:
    ---------
    Класс Link представляет собой базовую модель посещения ссылок
    сотрудником компании.

    Поля:
    -----
    employee - сотрудник
    links - ссылка
    time_transition - время перехода по ссылке

    """
    employee = models.ForeignKey('User',
                                 on_delete=models.CASCADE,
                                 verbose_name='сотрудник',
                                 blank=True)
    links = models.CharField(max_length=300,
                             verbose_name='ссылка')
    time_transition = models.DateTimeField(auto_now_add=True,
                                           verbose_name='время перехода')

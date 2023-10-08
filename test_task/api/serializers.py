from django.utils import timezone
from rest_framework import serializers
from .models import User, Link


class UserSerializer(serializers.ModelSerializer):
    """
    Описание:
    ---------
    Сериализатор для модели User.

    Атрибуты Meta класса:
    ---------------------
    model - используемая модель для сериализатора
    fields - определяет, какие поля модели или другого источника данных будут включены в сериализатор,
             и какие из них будут доступны для чтения (сериализации) или записи (десериализации)
    """
    class Meta:
        model = User
        fields = '__all__'


class LinkSerializer(serializers.ModelSerializer):
    """
    Описание:
    ---------
    Сериализатор для модели Link.

    Атрибуты Meta класса:
    ---------------------
    model - используемая модель для сериализатора
    fields - определяет, какие поля модели или другого источника данных будут включены в сериализатор,
             и какие из них будут доступны для чтения (сериализации) или записи (десериализации)
    """
    class Meta:
        model = Link
        fields = ['employee', 'links', 'time_transition']

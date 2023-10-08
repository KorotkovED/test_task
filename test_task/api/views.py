import re
from .serializers import UsersSerializer, LinkSerializer
from .models import User, Link
from rest_framework import status, permissions
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from django.core.exceptions import ValidationError
from datetime import datetime
from .filters import DomainsFilter
from django_filters import rest_framework as filters


class UserViewSet(ModelViewSet):
    """
    Описание:
    ---------
    Представление для модели User.

    Свойства:
    ---------
    queryset - коллекция объектов БД
    serilizer_class - сериализатор, используемый для преобразования объектов в Python
    permissions - class - список классов разрешений, которые определяют, кто имеет доступ к представлению

    Дополнительные методы:
    ----------------------
    visited_links - метод, который позволяет загрузить в БД все ссылки, на которые заходил сотрудник. Доступен только по запросу POST.
                    Принимаемые параметры: request - экземпляр класса HttpRequest, который представляет собой HTTP-запрос от клиента к серверу.
                                           pk: [int] - id сотрудника

    visited_domains - метод, который позволяет отобразить все уникальные домены, на которые заходил сотрудник, а также при указании доп. параметров from и to в запросе к API,
                      будут выведены все уникальные домены в указанном промежутке времени. Метод доступен только по запросу GET.
                      Принимаемые параметры: request - экземпляр класса HttpRequest, который представляет собой HTTP-запрос от клиента к серверу.
                                                pk: [int] - id сотрудника
    """
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = (permissions.IsAuthenticated,) 
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = DomainsFilter


    @action(methods=['POST'], detail=False, url_path='visited_links')
    def visited_links(self, request, pk:[int]=None):
        """Посещенные сотрудником ссылки."""
        try:
            user = self.get_object()
            links_data = request.data.get('links', [])

            if not isinstance(links_data, list):
                return Response({'status': 'BAD_REQUEST'},
                                status=status.HTTP_400_BAD_REQUEST)

            link_dicts = [{'employee': user.pk, 'links': link} for link in links_data]

            serializer = LinkSerializer(data=link_dicts, many=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'status': 'BAD_REQUEST'},
                                status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'status': 'HTTP_404_NOT_FOUND'},
                            status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            return Response({'status': 'BAD_REQUEST', 'error': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)


    @action(methods=['GET'], detail=False, url_path='visited_domains')
    def visited_domains(self, request, pk:[int]):
        """Метод для получения уникальных доменов."""
        try:
            time_from = request.query_params.get('from')
            time_to = request.query_params.get('to')
            if time_from and time_to:
                time_from = datetime.utcfromtimestamp(int(time_from))
                time_to = datetime.utcfromtimestamp(int(time_to))

                links = Link.objects.filter(time_transition__gte=time_from, time_transition__lte=time_to)
            else:
                
                links = Link.objects.filter(employee = pk)

            domain_regex = r"https?:\/\/([^\/]+)"

            domains = []
            for link in links:
                matches = re.findall(domain_regex, link.links)
                if matches:
                    domains.append(matches[0])

            unique_domains = []

            for item in domains:
                if item not in unique_domains:
                    unique_domains.append(item)

            return Response({'domains': unique_domains,
                             'status': 'ok'}, status=status.HTTP_200_OK)
        except Link.DoesNotExist:
            return Response({'status': 'HTTP_404_NOT_FOUND'}, status=status.HTTP_404_NOT_FOUND)

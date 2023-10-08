from django.urls import path, include, re_path
from .views import UserViewSet
from rest_framework.routers import DefaultRouter

app_name = 'api'

router = DefaultRouter()

router.register(r'user', UserViewSet)

urlpatterns = [
    re_path(r'^v1/user/(?P<pk>[0-9]+)/visited_links/$', 
            UserViewSet.as_view({'post': 'visited_links'}),
            name='user-visited-links'),
    re_path(r'^v1/user/(?P<pk>[0-9]+)/visited_domains/$', 
            UserViewSet.as_view({'get': 'visited_domains'}),
            name='user-visited-domains'),
    path('v1/', include(router.urls))
]

from django.urls import include, path
from django.contrib import admin
# from rest_framework.routers import DefaultRouter

# from cats.views import CatViewSet


# router = DefaultRouter()
# router.register('cats', CatViewSet)

urlpatterns = [
    # path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('', include('cats.urls', namespace='cats'))
]
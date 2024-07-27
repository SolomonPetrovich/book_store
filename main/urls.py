from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import  ActivateUser, BookViewSet, ReviewViewSet


router = DefaultRouter()
router.register('books', BookViewSet)
router.register('reviews', ReviewViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('auth/activate/<uid>/<token>', ActivateUser.as_view({'get': 'activation'}), name='activation'),
]

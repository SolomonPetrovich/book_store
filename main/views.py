from rest_framework import viewsets, status
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Book, Review
from .serializers import BookSerializer, ReviewSerializer
from .permission import IsAuthenticatedOrReadOnly
from djoser.views import UserViewSet
from rest_framework.response import Response

class BookViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )

    @swagger_auto_schema(
        operation_description="Add a book to the user's favorites",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={},
            required=[],
            description="This endpoint does not require a request body."
        ),
        responses={
            200: 'Book added to favorites',
            400: 'Book already in favorites or UUID not provided',
            401: 'User not authenticated'
        }
    )
    @action(detail=True, methods=['post'])
    def add_to_fav(self, request, pk=None):
        book = self.get_object()
        user = request.user

        if book.favorite.filter(id=user.id).exists():
            return Response({'status': 'Book already in favorites'}, status=status.HTTP_400_BAD_REQUEST)

        book.favorite.add(user)
        book.save()
        return Response({'status': 'Book added to favorites'}, status=status.HTTP_200_OK)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        return super().perform_update(serializer)
    
    def perform_destroy(self, instance):
        return super().perform_destroy(instance)
    


 
class ActivateUser(UserViewSet):
    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())
 
        kwargs['data'] = {"uid": self.kwargs['uid'], "token": self.kwargs['token']}
 
        return serializer_class(*args, **kwargs)
 
    def activation(self, request, uid, token, *args, **kwargs):
        super().activation(request, *args, **kwargs)
        return Response(status=status.HTTP_204_NO_CONTENT)
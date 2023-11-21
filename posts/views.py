from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from posts.models import Post, Like
from posts.permissions import IsPostAuthor
from posts.serializers import PostSerializers, DateRangeSerializer, LikeAnalyticSerializer


# Create your views here.
class PostsViewSet(ModelViewSet):
    queryset = Post.objects.select_related('author').all()
    serializer_class = PostSerializers
    permission_classes = (IsAuthenticated, )
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated, IsPostAuthor]
        return super().get_permissions()

    @action(methods=['post'], detail=True, url_name=r'like', url_path='like')
    def like_post(self, request, **kwargs):
        post = self.get_object()
        post.likes.add(request.user)
        return Response(data={'likes_count': post.likes_count}, status=status.HTTP_201_CREATED)

    @action(methods=['post'], detail=True, url_name=r'unlike', url_path='unlike')
    def unlike_post(self, request, **kwargs):
        post = self.get_object()
        post.likes.remove(request.user)
        return Response(data={'likes_count': post.likes_count}, status=status.HTTP_204_NO_CONTENT)


class PostsAnalyticsView(ListAPIView):

    permission_classes = (IsAuthenticated, )
    serializer_class = LikeAnalyticSerializer

    def get_queryset(self):
        queryset = Like.objects.test_aggregation(user=self.request.user)

        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date', timezone.now().date().isoformat())

        data = {
            "start_date": start_date,
            "end_date": end_date,
        }

        date_serializer = DateRangeSerializer(data=data)
        date_serializer.is_valid(raise_exception=True)

        if start_date and end_date:
            queryset = queryset.filter(created_at__date__range=(start_date, end_date))

        else:
            queryset = queryset.filter(created_at__date__lte=end_date)

        return queryset

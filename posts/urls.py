from django.urls import path, include
from rest_framework.routers import DefaultRouter

from posts.views import PostsViewSet, PostsAnalyticsView

router = DefaultRouter()
router.register(r'posts', PostsViewSet, basename='posts')

urlpatterns = [
    path('', include(router.urls)),
    path('analytics/', PostsAnalyticsView.as_view(), name='analytics'),

]

from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework import status
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt import views as jwt_views

from users.permissions import NotAuthenticated
from users.serializers import (SignUpSerializer, LogOutSerializer, UserActivitySerializer,
                               UserActivityQueryParamSerializer)


class SignUpView(CreateAPIView):
    queryset = get_user_model().objects.all()
    permission_classes = (NotAuthenticated, )
    serializer_class = SignUpSerializer


class LogInView(jwt_views.TokenObtainPairView):
    permission_classes = (NotAuthenticated, )


class LogOutView(APIView):
    serializer_class = LogOutSerializer
    permission_classes = (IsAuthenticated, )

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data={'Logged out'}, status=status.HTTP_204_NO_CONTENT)


class UserActivityView(APIView):

    permission_classes = (IsAuthenticated, )

    def get(self, request, **kwargs):
        """
        Query param user_id -- Pass user id, to see his last activity
        """
        query_param_serializer = UserActivityQueryParamSerializer(data=self.request.query_params)
        query_param_serializer.is_valid(raise_exception=True)

        user_id = self.request.query_params.get('user_id')
        user = get_object_or_404(get_user_model(), pk=user_id)
        user_key = f'user__{user_id}'

        if cached_user_date := cache.get(user_key):
            last_request_time = cached_user_date
        else:
            last_request_time = user.last_request_time

        data = {'last_login': user.last_login, 'last_request_time': last_request_time}
        serializer = UserActivitySerializer(data=data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data)

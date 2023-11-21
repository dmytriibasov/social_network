from rest_framework import serializers

from posts.models import Post
from users.serializers import SimpleUserSerializerData


class PostSerializers(serializers.ModelSerializer):
    likes_count = serializers.IntegerField(read_only=True)
    author_data = SimpleUserSerializerData(source='author', read_only=True)

    class Meta:
        model = Post
        read_only_fields = ['created_at', 'updated_at']
        exclude = ['likes', 'author']


class DateRangeSerializer(serializers.Serializer):
    start_date = serializers.DateField(required=False, allow_null=True)
    end_date = serializers.DateField(required=False)

    def validate(self, data):
        if data.get('start_date'):
            if data['start_date'] > data['end_date']:
                raise serializers.ValidationError('Start date must come earlier than end date')
        return data


class LikeAnalyticSerializer(serializers.Serializer):
    day = serializers.DateTimeField(format='%Y-%m-%d')
    likes_count = serializers.IntegerField()

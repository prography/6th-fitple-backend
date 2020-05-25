from rest_framework import serializers
from .models import Team, Comment


class TeamSerializer(serializers.ModelSerializer):
    author = serializers.CharField(read_only=True)

    class Meta:
        model = Team
        fields = ('author', 'id', 'title', 'description', 'status', 'personnel', 'region', 'goal', 'kind',
                  'people', 'image', 'created_at', 'modified_at')
        read_only_fields = ['author']


class TeamListSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        model = Team
        fields = ('author', 'id', 'title', 'description', 'image')


#이거의 역할을 아직 모르겠다
class RecursiveSerializer(serializers.Serializer):
    def to_representation(self, instance):
        serializer = self.parent.parent.__class__(instance, context=self.context)
        return serializer.data


class CommentSerializer(serializers.ModelSerializer):
    reply = serializers.SerializerMethodField()
    user = serializers.CharField(read_only=True)

    class Meta:
        model = Comment
        fields = ('team', 'id', 'user', 'parent', 'comment', 'created_at', 'is_deleted', 'reply')
        read_only_fields = ['user']

    def get_reply(self, instance):
        serializer = self.__class__(instance.reply, many=True)
        serializer.bind('', self)
        return serializer.data

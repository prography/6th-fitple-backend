from rest_framework import serializers
from .models import Team, Comment


class TeamListSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        model = Team
        fields = ('author', 'id', 'title', 'description', 'image')


class TeamSerializer(serializers.ModelSerializer):
    author = serializers.CharField(read_only=True)

    class Meta:
        model = Team
        fields = ('author', 'id', 'title', 'description', 'status', 'planner', 'developer', 'designer',
                  'region', 'goal', 'kind', 'people', 'image', 'created_at', 'modified_at')
        read_only_fields = ['author']


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


class TeamOnlyCommentSerializer(serializers.ModelSerializer):
    parent_comments = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = ('id', 'parent_comments')

    def get_parent_comments(self, obj):
        parent_comments = obj.comments.filter(parent=None)
        serializer = CommentSerializer(parent_comments, many=True)
        return serializer.data

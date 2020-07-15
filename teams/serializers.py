from rest_framework import serializers

from accounts.serializers import UserSimpleSerializerVerTwo
from applications.models import TeamApplication
from .models import Team, Comment, Image


## test
class ImageSerializer(serializers.ModelSerializer):
    image = serializers.FileField(required=False)

    class Meta:
        model = Image
        fields = ('id', 'name', 'image')


class TeamListSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = ('author', 'id', 'title', 'description', 'region', 'image')

    def get_author(self, obj):
        return {
            "id": obj.author.id,
            "username": obj.author.username,
            "image": obj.author.profile.image.url
        }


class TeamSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    # author = serializers.CharField(read_only=True)  # read_only=True
    image = serializers.FileField(required=False)

    # question = JoinQuestionsSerializer(write_only=True) # 팀 생성할 때만

    class Meta:
        model = Team
        fields = ('author', 'id', 'title', 'description', 'planner', 'developer', 'designer',
                  'region', 'goal', 'image', 'created_at', 'modified_at', 'active_status')

    def get_author(self, obj):
        return {
            "id": obj.author.id,
            "username": obj.author.username,
            "image": obj.author.profile.image.url
        }


class CommentSerializer(serializers.ModelSerializer):
    reply = serializers.SerializerMethodField()
    user = UserSimpleSerializerVerTwo(read_only=True)

    # serializers.CharField(read_only=True)

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


class TeamMemberSimpleSerializer(serializers.ModelSerializer):
    team_id = serializers.SerializerMethodField()
    team_title = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()

    class Meta:
        model = TeamApplication
        fields = ['team_id', 'team_title', 'role']

    def get_team_id(self, obj):  # TeamApplication
        return obj.team.id

    def get_team_title(self, obj):  # TeamApplication
        return obj.team.title

    def get_role(self, obj):
        return "팀원"


class TeamLeaderSimpleSerializer(serializers.ModelSerializer):
    team_id = serializers.SerializerMethodField()
    team_title = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = ['team_id', 'team_title', 'role']

    def get_team_id(self, obj):  # TeamApplication
        return obj.id

    def get_team_title(self, obj):  # TeamApplication
        return obj.title

    def get_role(self, obj):
        return "팀장"

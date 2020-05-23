from rest_framework import serializers
from .models import Team


class TeamSerializer(serializers.ModelSerializer):
    author = serializers.CharField(read_only=True)

    class Meta:
        model = Team
        fields = ('author', 'id', 'title', 'description', 'status', 'personnel', 'region', 'goal', 'kind',
                  'people', 'image', 'created_at', 'modified_at')
        read_only_fields = ['author']


class TeamListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('author', 'id', 'title', 'description', 'image')

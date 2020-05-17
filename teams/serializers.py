from rest_framework import serializers
from .models import Team


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('author', 'title', 'description', 'status', 'personnel', 'region', 'goal', 'kind',
                  'people', 'image', 'created_at', 'modified_at')

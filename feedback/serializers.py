from rest_framework import serializers

from .models import Feedback


class FeedbackSerializers(serializers.Serializer):
    feedback = serializers.CharField(required=True)

    def create(self, validated_data):
        feedback = Feedback.objects.create(
            feedback=validated_data['feedback']
        )
        feedback.save()
        return "ok"
